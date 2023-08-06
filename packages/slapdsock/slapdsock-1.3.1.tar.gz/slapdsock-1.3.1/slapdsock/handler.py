# -*- coding: ascii -*-
"""
slapdsock.handler - request handler

slapdsock - OpenLDAP back-sock listeners with Python
see https://code.stroeder.com/pymod/python-slapdsock

(c) 2015-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

#-----------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------

# from Python's standard lib
import sys
import pwd
import struct
import time
import socket
import logging
import inspect
import datetime
from socketserver import BaseRequestHandler

import ldap0.functions
from ldap0.base import encode_entry_dict

# internal import from slapsock
import slapdsock.message
from .message import ENTRYResponse, RESULTResponse, InternalErrorResponse, CONTINUE_RESPONSE

#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------

__all__ = [
    'SlapdSockHandler',
    'NoopHandler',
]

SO_PEERCRED_DICT = {
    'linux': (17, '3i'),  # for Linux systems
}


#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------


class SlapdSockHandlerError(Exception):
    """
    Exception class to be raised within handler methods
    """

    def __init__(
            self,
            msg: str,
            log_level: int = None,
            response=None,
            log_vars=None,
    ):
        Exception.__init__(self)
        self.msg = msg
        self.log_level = log_level
        self.log_args = (())
        self.response = response
        # Store the logged vars
        log_vars = log_vars or []
        # Get the local variables dict of the caller
        frame = inspect.currentframe()
        try:
            var_dict = frame.f_back.f_locals
        finally:
            del frame
        # Store dict of only the debug vars
        self.log_vars = {
            log_var: var_dict[log_var]
            for log_var in log_vars
            if log_var in var_dict
        }

    def log(self, logger):
        """
        Write exception log message to logger
        """
        log_debug = logger.getEffectiveLevel() <= logging.DEBUG
        if log_debug:
            # only at DEBUG level
            for var_name, var_value in self.log_vars.items():
                logger.debug('%s = %r', var_name, var_value)
        if self.log_args:
            logger.log(
                self.log_level,
                *self.log_args,
                exc_info=(self.log_level >= logging.ERROR)
            )
        logger.log(
            self.log_level,
            '%s => response %r',
            self.msg,
            self.response,
            exc_info=log_debug,
        )


class SlapdSockHandler(BaseRequestHandler):

    """
    Base class for a handler receiving requests from
    OpenLDAP's back-sock.

    Note that when using this class as base class you have to implement
    a method for all request types hitting your handler.
    """

    cache_ttl = {}

    def __init__(self, *args, **kwargs):
        self._logged_vars = set()
        # We need current time in GeneralizedTime syntax later
        self.now_dt = datetime.datetime.utcnow()
        self.now_str = ldap0.functions.datetime2str(self.now_dt)
        BaseRequestHandler.__init__(self, *args, **kwargs)

    def _get_peer_cred(self):
        """
        Currently works only on Linux
        """
        try:
            so_num, struct_fmt = SO_PEERCRED_DICT[sys.platform]
        except KeyError:
            return None, None, None
        peer_creds_struct = self.request.getsockopt(
            socket.SOL_SOCKET,
            so_num,
            struct.calcsize(struct_fmt)
        )
        return struct.unpack(struct_fmt, peer_creds_struct)
        # _get_peer_cred()

    def _check_access(self, uid=None):
        """
        Check whether the POSIX-UID shall be granted access
        """
        if self.peer_uid in self.server._allowed_uids:
            self._log(
                logging.DEBUG,
                'Access granted for peer UID %d',
                self.peer_uid
            )
            result = True
        elif self.peer_gid in self.server._allowed_gids:
            self._log(
                logging.DEBUG,
                'Access granted for peer GID %d',
                self.peer_gid
            )
            result = True
        elif uid is not None:
            # Try to map numeric peer's uidNumber to known system user
            try:
                peer_pwd = pwd.getpwuid(self.peer_uid)
            except KeyError:
                self._log(
                    logging.WARN,
                    'Username for peer UID %d not found',
                    self.peer_uid
                )
                result = False
            else:
                # Now we know the username of the peer's UID
                self._log(logging.DEBUG, 'peer_pwd.pw_name = %r', peer_pwd.pw_name)
                result = peer_pwd.pw_name == uid
        else:
            result = False
        return result  # _check_access()

    def _log(self, log_level, *args, **kwargs):
        """
        Wrapper method adding log prefix
        """
        # Log variables
        if self.server.logger.getEffectiveLevel() <= logging.DEBUG:
            frame = inspect.currentframe()
            try:
                all_vars = frame.f_back.f_locals
            finally:
                del frame
            for var_name in self.server._log_vars:
                if var_name in all_vars and not var_name in self._logged_vars:
                    self._logged_vars.add(var_name)
                    self._log(logging.DEBUG, '%s = %r', var_name, all_vars[var_name])
        # Log the real stuff
        self.server.logger.log(
            log_level,
            ' '.join((self.log_prefix, args[0])),
            *args[1:],
            **kwargs
        )

    def do_monitor(self, request):
        """
        Return ENTRY response with monitoring data in response
        to MONITOR request
        """
        # Check authorization of calling process based on Unix peer credentials
        if not self._check_access():
            error_message = 'Peer {:d}/{:d} not authorized to query monitor'.format(
                self.peer_uid,
                self.peer_gid,
            )
            self._log(logging.ERROR, error_message)
            return RESULTResponse(
                request.msgid,
                'insufficientAccessRights',
                info=error_message
            )
        monitor_entry = self.server.monitor_entry()
        self._log(logging.DEBUG, 'self.server._monitor_dn = %r', self.server._monitor_dn)
        self._log(logging.DEBUG, 'monitor_entry = %r', monitor_entry)
        return ENTRYResponse(
            request.msgid,
            self.server._monitor_dn.encode('utf-8'),
            encode_entry_dict(monitor_entry),
        )
        # end of do_monitor ()

    def handle(self):
        """
        Handle the incoming request
        """
        self.request_timestamp = time.time()
        self.server._req_count += 1
        msgid = None
        # Generate basic log prefix here
        self.log_prefix = str(id(self))
        reqtype = '-/-'

        try: # -> Exception
            self.peer_pid, self.peer_uid, self.peer_gid = self._get_peer_cred()
            self._log(
                logging.DEBUG,
                '----- incoming request via %r from pid=%s uid=%s gid=%s -----',
                self.request.getsockname(),
                self.peer_pid, self.peer_uid, self.peer_gid,
            )
            request_data = self.request.recv(500000)
            if __debug__:
                # Security advice:
                # Request data can contain clear-text passwords!
                self._log(logging.DEBUG, 'request_data = %r', request_data)
            self.server._bytes_received += len(request_data)
            req_lines = request_data.split(b'\n')
            # Extract request type
            reqtype = req_lines[0].decode('ascii')
            self._log(logging.DEBUG, 'reqtype = %r', reqtype)
            # Get the request message class
            request_class = getattr(slapdsock.message, '%sRequest' % reqtype)
            self._log(logging.DEBUG, 'request_class=%r', request_class)
            # Extract the request message
            sock_req = request_class(req_lines)
            # Update request counter for request type
            self.server._req_counters[reqtype.lower()] += 1
            if __debug__:
                # Security advice:
                # Request data can contain sensitive data
                # (e.g. BIND with password) => never run in debug mode!
                self._log(logging.DEBUG, 'sock_req = %r // %r', sock_req, sock_req.__dict__)
            # Generate the request specific log prefix here
            self.log_prefix = sock_req.log_prefix(self.log_prefix)
            msgid = sock_req.msgid
            cache_key = sock_req.cache_key()

            try: # -> SlapdSockHandlerError

                try: # Try cache
                    response = self.server.req_cache[reqtype][cache_key]
                except KeyError:
                    self._log(logging.DEBUG, 'Request not cached: cache_key = %r', cache_key)
                    # Get the handler method in own class
                    handle_method = getattr(self, 'do_%s' % reqtype.lower())
                    # Let the handler method generate a response message
                    response = handle_method(sock_req)
                    if cache_key and reqtype in self.server.req_cache:
                        # Store response in cache
                        self.server.req_cache[reqtype][cache_key] = response
                        self._log(
                            logging.DEBUG,
                            'Response stored in cache: cache_key = %r',
                            cache_key,
                        )

                else:
                    self._log(logging.DEBUG, 'Response from cache: cache_key = %r', cache_key)

            except SlapdSockHandlerError as handler_exc:
                handler_exc.log(self.server.logger)
                response = handler_exc.response or InternalErrorResponse(msgid)

        except Exception:
            self._log(
                logging.ERROR,
                'Unhandled exception during processing request:',
                exc_info=True
            )
            response = InternalErrorResponse(msgid)
        try:
            # Serialize the response instance
            if isinstance(response, str):
                response_str = response.encode('utf-8')
            else:
                response_str = bytes(response)
            self._log(logging.DEBUG, 'response_str = %r', response_str)
            if response_str:
                self.request.sendall(response_str)
        except Exception:
            self._log(
                logging.ERROR,
                'Unhandled exception while sending response:',
                exc_info=True
            )
        else:
            response_delay = time.time()-self.request_timestamp
            self.server.update_monitor_data(len(response_str), response_delay)
            self._log(logging.DEBUG, 'response_delay = %0.3f', response_delay)
        # end of handle()


class NoopHandler(SlapdSockHandler):

    """
    This handler simply returns CONTINUE+LF for every sockops request
    and empty string for sockresps and unbind requests.

    This is handy to be used as safe base class for own custom handler
    to make sure each back-sock request is always answered in
    case of misconfigured "overlay sock" section.
    """

    def do_add(self, request):
        """
        ADD
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_bind(self, request):
        """
        BIND
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_compare(self, request):
        """
        COMPARE
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_delete(self, request):
        """
        DELETE
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_modify(self, request):
        """
        MODIFY
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_modrdn(self, request):
        """
        MODRDN
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_search(self, request):
        """
        SEARCH
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE

    def do_unbind(self, request):
        """
        UNBIND
        """
        _ = (self, request) # pylint dummy
        return ''

    def do_result(self, request):
        """
        RESULT
        """
        _ = (self, request) # pylint dummy
        return ''

    def do_entry(self, request):
        """
        ENTRY
        """
        _ = (self, request) # pylint dummy
        return ''

    def do_extended(self, request):
        """
        EXTERNAL
        """
        _ = (self, request) # pylint dummy
        return CONTINUE_RESPONSE
