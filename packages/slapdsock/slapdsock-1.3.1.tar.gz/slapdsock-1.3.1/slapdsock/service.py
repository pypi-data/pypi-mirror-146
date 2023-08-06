# -*- coding: ascii -*-
"""
slapdsock.service - The Unix domain listener

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
import grp
import os
import pwd
import socket
import datetime
import threading
from queue import Queue
from socketserver import UnixStreamServer, ThreadingMixIn
from collections import defaultdict

# from ldap0 package
import ldap0.functions
from ldap0.lock import LDAPLock
from ldap0.cache import Cache

from .ldaphelper import ldap_float_str, LocalLDAPConn

#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------

class SlapdSockServer(UnixStreamServer, LocalLDAPConn, ThreadingMixIn):
    """
    Base class for a Unix domain socket server implementing
    an external back-sock listener
    """

    __slots__ = (
        '_allowed_gids',
        '_allowed_uids',
        '_average_count',
        '_avg_response_time',
        '_bytes_received',
        '_bytes_sent',
        '_ldapi_conn',
        '_ldapi_conn_lock',
        'logger',
        '_log_vars',
        'max_req_cache_time',
        '_max_response_time',
        '_monitor_dn',
        'req_cache',
        '_req_count',
        '_req_counters',
        'req_threads_active',
        'requests',
        '_socket_permissions',
        '_socket_timeout',
        '_start_time',
        'thread_pool_size',
    )

    allow_reuse_address = True

    def __init__(
            self,
            server_address,
            handler_class,
            logger,
            average_count,
            socket_timeout,
            socket_permissions,
            allowed_uids,
            allowed_gids,
            bind_and_activate=True,
            monitor_dn='cn=sock-monitor',
            log_vars=None,
            thread_pool_size=1,
        ):
        # Initialize cache per request type
        self.req_cache = {}
        for reqtype, cache_ttl in handler_class.cache_ttl.items():
            if cache_ttl > 0:
                self.req_cache[reqtype] = Cache(ttl=cache_ttl)
        self.max_req_cache_time = 0.0
        self.logger = logger
        self._socket_timeout = socket_timeout
        self._socket_permissions = socket_permissions
        UnixStreamServer.__init__(
            self, server_address, handler_class, bind_and_activate
        )
        LocalLDAPConn.__init__(self, logger)
        self.logger.info(
            'Initializing %s instance listening on %r',
            self.__class__.__name__,
            server_address,
        )
        self._average_count = average_count
        self._start_time = datetime.datetime.utcnow()
        # Global request counter
        self._req_count = 0
        # Request counter dict per request type
        self._req_counters = defaultdict(lambda: 0)
        self._bytes_sent = 0
        self._bytes_received = 0
        self._avg_response_time = 0.0
        self._max_response_time = 0.0
        self._allowed_uids = self._map_names(
            pwd.getpwnam,
            pwd.getpwuid,
            allowed_uids
        )
        self._allowed_gids = self._map_names(
            grp.getgrnam,
            grp.getgrgid,
            allowed_gids
        )
        self._monitor_dn = monitor_dn or 'cn=%s' % (self.__class__.__name__)
        self._log_vars = sorted(log_vars or [])
        self.logger.debug('%s.log_vars=%s', self.__class__.__name__, log_vars)
        # For lazy LDAPI connecting in self.get_ldapi_conn()
        self._ldapi_conn = None
        self._ldapi_conn_lock = LDAPLock(desc='get_ldapi_conn() in %r' % (self.__class__,))
        # thread pool initialization
        self.req_threads_active = self.req_threads_max = 0
        self.thread_pool_size = thread_pool_size
        self.requests = Queue(self.thread_pool_size)
        # end of SlapdSockServer()

    def _map_names(self, map_name_func, map_id_func, nameorid_list):
        """
        Map user or group names to their POSIX id
        """
        id_set = set()
        for i in nameorid_list:
            if isinstance(i, int):
                try:
                    map_id_func(i)
                except KeyError:
                    self.logger.warning('Name for allowed ID %d not found', i)
                else:
                    id_set.add(i)
            elif isinstance(i, str):
                try:
                    mapped_id = map_name_func(i)[2]
                except KeyError:
                    self.logger.warning('ID for allowed name %r not found', i)
                else:
                    id_set.add(mapped_id)
        self.logger.debug(
            '%s ID set: %s',
            map_name_func.__name__,
            ','.join([str(posix_id) for posix_id in id_set]),
        )
        return id_set

    def update_monitor_data(self, r_len, r_delay):
        """
        Update some monitoring data
        """
        self._bytes_sent += r_len
        self._avg_response_time = (
            (self._average_count - 1) * self._avg_response_time + r_delay
        ) / self._average_count
        self._max_response_time = max(
            self._max_response_time,
            r_delay
        )

    def monitor_entry(self):
        """
        Returns entry dictionary with monitoring data.

        Override this method to extend the monitor entry with additional
        attributes.
        """
        monitor_entry = {
            'sockPythonDebug': [str(__debug__)],
            'sockLogLevel': [str(self.logger.getEffectiveLevel())],
            'sockThreadCount': [str(threading.active_count())],
            'sockStartTime': [ldap0.functions.datetime2str(self._start_time)],
            'sockCurrentTime': [ldap0.functions.datetime2str(datetime.datetime.utcnow())],
            # Request counters
            'sockRequestAll': [str(self._req_count)],
            # Byte counters
            'sockBytesReceived': [str(self._bytes_received)],
            'sockBytesSent': [str(self._bytes_sent)],
            # Response times
            'sockAvgResponseTime': [ldap_float_str(self._avg_response_time)],
            'sockMaxResponseTime': [ldap_float_str(self._max_response_time)],
            'sockLDAPIConnection': [repr(self._ldapi_conn)],
        }
        if self._ldapi_conn:
            monitor_entry['sockLDAPIAuthzID'] = [self._ldapi_conn.whoami_s()]
        else:
            monitor_entry['sockLDAPIAuthzID'] = ['None']
        # Counters per request type
        for req_type, req_counter in sorted(self._req_counters.items()):
            req_type_str = req_type[0].upper(), req_type[1:].lower()
            monitor_entry['sockRequest%s%sCount' % ((req_type_str))] = [str(req_counter)]
        # Caches per request type
        for req_type, req_cache in sorted(self.req_cache.items()):
            req_type_str = req_type[0].upper(), req_type[1:].lower()
            monitor_entry.update({
                'sockCache%s%sNum' % req_type_str: [str(len(req_cache))],
                'sockCache%s%sTTL' % req_type_str: [ldap_float_str(req_cache._ttl)],
                'sockCache%s%sHitCount' % req_type_str: [str(req_cache.hit_count)],
            })
            if self._req_counters[req_type]:
                monitor_entry['sockCache%s%sHitRate' % (
                    (req_type_str)
                )] = [ldap_float_str(req_cache.hit_ratio)]
            else:
                monitor_entry['sockCache%s%sHitRate' % (
                    (req_type_str)
                )] = [ldap_float_str(0.0)]
        return monitor_entry

    def server_bind(self):
        """Override server_bind to set socket options."""
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(self._socket_timeout)
        try:
            os.unlink(self.server_address)
        except OSError as os_error:
            if os.path.exists(self.server_address):
                raise os_error
        UnixStreamServer.server_bind(self)
        os.chmod(self.server_address, int(self._socket_permissions, 8))
        # end of server_bind()

    def serve_forever(self):
        # set up the threadpool
        for _ in range(self.thread_pool_size):
            req_thread = threading.Thread(target=self.process_request_thread)
            req_thread.daemon = True
            req_thread.start()
        # server main loop
        while True:
            self.handle_request()
        self.server_close()

    def process_request_thread(self):
        """
        obtain request from queue instead of directly from server socket
        """
        while True:
            threads = self.requests.get()
            self.req_threads_active = len(threads)
            if self.req_threads_active > self.req_threads_max:
                self.req_threads_max = self.req_threads_active
            ThreadingMixIn.process_request_thread(self, *threads)

    def handle_request(self):
        """
        simply collect requests and put them on the queue for the workers.
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.logger.debug('Queuing new request: %r %r', request, client_address)
            self.requests.put((request, client_address))
