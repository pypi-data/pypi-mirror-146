# -*- coding: ascii -*-
"""
slapdsock.message - Processing messages received/returned from/to OpenLDAP's back-sock

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
import hashlib
from base64 import b64decode
from io import BytesIO
from typing import List

# from ldap0 package
from ldap0.ldif import LDIFParser, LDIFWriter
from ldap0 import LDAPError

from .ldaphelper import RESULT_CODE

#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------

__all__ = [
    'CONTINUE_RESPONSE',
    'ListFile',
    'SockRequest',
    'ADDRequest',
    'BINDRequest',
    'COMPARERequest',
    'DELETERequest',
    'MODIFYRequest',
    'MODRDNRequest',
    'RESULTRequest',
    'ENTRYRequest',
    'SEARCHRequest',
    'UNBINDRequest',
    'SockResponse',
    'RESULTResponse',
    'ENTRYResponse',
    'CompareFalseResponse',
    'CompareTrueResponse',
    'NoSuchObjectResponse',
    'InvalidCredentialsResponse',
    'UnwillingToPerformResponse',
    'SuccessResponse',
    'InternalErrorResponse',
    'InvalidAttributeSyntaxResponse',
]

CONTINUE_RESPONSE = b'CONTINUE\n'


#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------


def ldap_str(buf: bytes) -> str:
    """
    Decode the byte-sequence in :buf: to str object
    """
    return buf.decode('utf-8')


def ldap_attrs(attrs_str: bytes) -> List[str]:
    """
    Return attribute list (for search requests)
    """
    if attrs_str == b'ALL':
        return '*'
    return attrs_str.decode('utf-8').split(' ')


class ListFile:
    """
    File-like object with readline method returning lines from a list
    of strings
    """

    def __init__(self, lines, line_counter=0):
        self._lines = lines
        self._line_counter = line_counter

    def readline(self):
        """
        Read a single line without trailing space
        """
        if self._line_counter >= len(self._lines):
            line = ''
        else:
            line = self._lines[self._line_counter]
            self._line_counter += 1
        return line


class SockRequest:

    """
    Base class for request messages sent by OpenLDAP's back-sock
    """

    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
    }
    cache_key_attrs = tuple()

    def __init__(self, req_lines):
        self._req_lines = req_lines
        self.reqtype = req_lines[0].decode('ascii')
        self._linecount = 1
        self._get_attrs()

    def _get_attrs(self):
        """
        Read the class attributes from the message line list
        """
        while self._req_lines[self._linecount]:
            try:
                key, val = self._req_lines[self._linecount].split(b': ', 1)
            except ValueError:
                break
            key = key.decode('ascii')
            if not key in self.req_attrs:
                break
            setattr(self, key, self.req_attrs[key](val))
            self._linecount += 1
        # end of ._get_attrs()

    def __bytes__(self) -> bytes:
        return b'\n'.join(self._req_lines)

    def cache_key(self):
        """
        Generated a hash-able cache key from the request data.

        Do not put secure data into the cache key
        when overriding this method!
        """
        if not self.cache_key_attrs:
            return None
        cache_attrs_list = []
        for attr in self.cache_key_attrs:
            try:
                cache_attrs_list.append((attr, getattr(self, attr)))
            except AttributeError:
                pass
        return tuple(cache_attrs_list)

    def log_prefix(self, prefix):
        """
        Return a logging prefix string
        """
        result = [prefix]
        for attr_name in ('connid', 'msgid'):
            try:
                val = getattr(self, attr_name)
            except AttributeError:
                pass
            else:
                result.append('%s = %r' % (attr_name, val))
        return ' '.join(result)


class MONITORRequest(SockRequest):

    """
    For manually injected MONITOR requests
    """

    def __init__(self, req_lines):
        SockRequest.__init__(self, req_lines)
        self.msgid = 0


class ADDRequest(SockRequest):

    """
    ADD
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    <entry in LDIF format>
    <blank line>
    """

    def _parse_ldif(self, linecount, max_entries=1):
        """
        Parse the subsequent request lines (starting from :linecount: as
        LDIF records and return all in a single list.
        """
        lrl = LDIFParser(
            ListFile(self._req_lines, linecount),
            max_entries=max_entries,
        )
        return lrl.list_entry_records()

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        dn_b, self.entry = self._parse_ldif(self._linecount, max_entries=1)[0]
        self.dn = dn_b.decode('utf-8')


class BINDRequest(SockRequest):

    """
    BIND
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    dn: <DN>
    method: <method number>
    credlen: <length of <credentials>>
    cred: <credentials>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
        'dn': ldap_str,
        'method': int,
        'credlen': int,
        'cred': bytes,
    }
    cache_key_attrs = (
        'binddn',
        'ssf',
        'suffix',
        'dn',
        'method',
    )

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        cred_str_list = [self.cred]
        while self._req_lines[self._linecount]:
            cred_str_list.append(self._req_lines[self._linecount])
            self._linecount += 1
        self.cred = b'\n'.join(cred_str_list)
        if len(self.cred) != self.credlen:
            raise ValueError('credlen: %d does not fit byte count of cred: %r' % (
                self.credlen, self.cred,
            ))

    def cache_key(self):
        return SockRequest.cache_key(self) + \
               (('credhash', hashlib.new('sha512', self.cred).digest()), )


class EXTENDEDRequest(SockRequest):

    """
    EXTENDED
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    oid: <OID>
    valuelen: <length of <value>>
    value: <value>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
        'oid': ldap_str,
        'value': b64decode,
    }
    cache_key_attrs = (
        'binddn',
        'ssf',
        'suffix',
        'oid',
        'value',
    )

    def _get_attrs(self):
        self.value = None
        SockRequest._get_attrs(self)


class COMPARERequest(ADDRequest):

    """
    COMPARE
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    dn: <DN>
    <attribute>: <value>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
    }
    cache_key_attrs = (
        'binddn',
        'ssf',
        'suffix',
        'dn',
        'atype',
        'avalue',
    )

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        dn_b, entry = self._parse_ldif(self._linecount, max_entries=1)[0]
        self.dn = dn_b.decode('utf-8')
        assert len(entry) == 1, ValueError(
            'Only one assertion type allowed but, got %r' % (entry,)
        )
        atype: bytes = list(entry.keys())[0]
        self.atype: str = atype.decode('utf-8')
        assert len(entry[atype]) == 1, ValueError(
            'Only one assertion value allowed, got %r' % (entry[self.atype],)
        )
        self.avalue = entry[atype][0]


class DELETERequest(SockRequest):

    """
    DELETE
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    dn: <DN>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
        'dn': ldap_str,
    }


class MODIFYRequest(ADDRequest):

    """
    MODIFY
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    dn: <DN>
    <repeat {
        <"add"/"delete"/"replace">: <attribute>
        <repeat { <attribute>: <value> }>
        -
    }>
    <blank line>
    """

    def _parse_ldif(self, linecount, max_entries=1):
        """
        Parse the subsequent request lines (starting from :linecount: as
        LDIF records and return all in a single list.
        """
        self._req_lines.insert(linecount+1, b'changetype: modify')
        lrl = LDIFParser(
            ListFile(self._req_lines, linecount),
            max_entries=max_entries,
        )
        return lrl.list_change_records()

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        dn_b, self.modops, _ = self._parse_ldif(self._linecount, max_entries=1)[0]
        self.dn = dn_b.decode('utf-8')


class MODRDNRequest(SockRequest):

    """
    MODRDN
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    dn: <DN>
    newrdn: <new RDN>
    deleteoldrdn: <0 or 1>
    <if new superior is specified: "newSuperior: <DN>">
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
        'dn': ldap_str,
        'newrdn': ldap_str,
        'deleteoldrdn': int,
        'newSuperior': ldap_str,
    }


class RESULTRequest(SockRequest):

    """
    RESULT
    msgid: <message id>
    code: <integer>
    matched: <matched DN>
    info: <text>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'code': int,
        'matched': ldap_str,
        'info': ldap_str,
    }


class ENTRYRequest(ADDRequest):

    """
    ENTRY
    msgid: <message id>
    <entry in LDIF format>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
    }


class SEARCHRequest(SockRequest):

    """
    SEARCH
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    base: <base DN>
    scope: <0-2, see ldap.h>
    deref: <0-3, see ldap.h>
    sizelimit: <size limit>
    timelimit: <time limit>
    filter: <filter>
    attrsonly: <0 or 1>
    attrs: <"all" or space-separated attribute list>
    <blank line>
    """
    req_attrs = {
        'msgid': int,
        'binddn': ldap_str,
        'peername': ldap_str,
        'ssf': int,
        'connid': int,
        'suffix': ldap_str,
        'base': ldap_str,
        'scope': int,
        'deref': int,
        'sizelimit': int,
        'timelimit': int,
        'filter': ldap_str,
        'attrs': ldap_attrs,
    }
    cache_key_attrs = (
        'binddn',
        'ssf',
        'suffix',
        'base',
        'scope',
        'deref',
        'sizelimit',
        'timelimit',
        'filter',
        'attrs',
    )


class UNBINDRequest(SockRequest):

    """
    UNBIND
    msgid: <message id>
    <repeat { "suffix:" <database suffix DN> }>
    <blank line>
    """


class SockResponse:

    """
    Base class for response messages returned to OpenLDAP's back-sock
    """

    line_sep = b'\n'

    def __init__(self, resp_type, resp_lines=None):
        self._resp_type = resp_type
        self._resp_lines = resp_lines or []

    def __bytes__(self) -> bytes:
        lines = [self._resp_type.encode('ascii')]
        for key, val in self._resp_lines:
            if isinstance(key, str):
                key = key.encode('ascii')
            if isinstance(val, str):
                val = val.encode('utf-8')
            lines.append(
                b': '.join((key, val))

            )
        return self.line_sep.join(lines)


class RESULTResponse(SockResponse):

    """
    RESULT
    msgid: <message id>
    code: <integer>
    matched: <matched DN>
    info: <text>
    <blank line>
    """

    def __init__(self, msgid, code, matched=None, info=None):
        assert msgid is None or isinstance(msgid, int), ValueError(
            'Expected msgid to be None or int, got %r' % (msgid,)
        )
        msgid = msgid or 0
        if isinstance(code, int):
            pass
        elif isinstance(code, str):
            # result code specified by name
            code = RESULT_CODE[code]
        elif isinstance(code, LDAPError):
            # clone response args from LDAPError instance
            ldap_error = code
            code = RESULT_CODE.get(type(ldap_error), RESULT_CODE['other'])
            try:
                info = ldap_error.args[0]['info'].decode('utf-8')
            except (AttributeError, KeyError, IndexError):
                pass
            try:
                matched = ldap_error.args[0]['matched'].decode('utf-8')
            except (AttributeError, KeyError, IndexError):
                pass
        else:
            raise TypeError('Invalid type of argument code=%r' % (code,))
        assert isinstance(code, int), ValueError(
            'Argument code must be integer but was: %r' % (code,)
        )
        resp_lines = [
            #('msgid', str(msgid)),
            ('code', str(code)),
        ]
        if matched is not None:
            resp_lines.append((b'matched', matched.encode('utf-8')))
        if info is not None:
            resp_lines.append((b'info', info.encode('utf-8')))
        SockResponse.__init__(self, 'RESULT', resp_lines)


class ENTRYResponse(SockResponse):

    """
    ENTRY
    msgid: <message id>
    <entry in LDIF format>
    <blank line>
    """

    def __init__(self, msgid, dn, entry):
        resp_lines = []
        self._dn = dn
        self._entry = entry
        SockResponse.__init__(self, 'ENTRY', resp_lines)

    def __bytes__(self) -> bytes:
        str_fileobj = BytesIO()
        ldif_writer = LDIFWriter(str_fileobj)
        ldif_writer.unparse(self._dn, self._entry)
        ldif_str = str_fileobj.getvalue()
        str_fileobj.close()
        return b'\n'.join((
            SockResponse.__bytes__(self),
            ldif_str
        ))


class SuccessResponse(RESULTResponse):
    """
    Convenience wrapper class for returning success(0)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=0,
            matched=None,
            info=info
        )


class CompareFalseResponse(RESULTResponse):
    """
    Convenience wrapper class for returning compareFalse(5)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=5,
            matched=None,
            info=info
        )


class CompareTrueResponse(RESULTResponse):
    """
    Convenience wrapper class for returning compareTrue(6)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=6,
            matched=None,
            info=info
        )


class InvalidAttributeSyntaxResponse(RESULTResponse):
    """
    Convenience wrapper class for returning invalidAttributeSyntax(21)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=21,
            matched=None,
            info=info
        )


class ConstraintViolationResponse(RESULTResponse):
    """
    Convenience wrapper class for returning constraintViolation(19)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=19,
            matched=None,
            info=info
        )


class NoSuchObjectResponse(RESULTResponse):
    """
    Convenience wrapper class for returning noSuchObject(32)
    """

    def __init__(self, msgid, info=None, matched=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=32,
            matched=None,
            info=info
        )


class InvalidCredentialsResponse(RESULTResponse):
    """
    Convenience wrapper class for returning invalidCredentials(49)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=49,
            matched=None,
            info=info
        )


class UnwillingToPerformResponse(RESULTResponse):
    """
    Convenience wrapper class for returning unwillingToPerform(53)
    """

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(
            self,
            msgid,
            code=53,
            matched=None,
            info=info
        )


class InternalErrorResponse(UnwillingToPerformResponse):
    """
    Convenience wrapper class for returning unwillingToPerform(53) and
    diagnostic message 'internal error'
    """

    def __init__(self, msgid, info=None):
        UnwillingToPerformResponse.__init__(
            self,
            msgid,
            info=info or 'internal error'
        )
