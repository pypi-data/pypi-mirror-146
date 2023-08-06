# -*- coding: ascii -*-
"""
slapd.ldaphelper - Helper stuff for LDAP access

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

# from ldap0 package
import ldap0
from ldap0.ldapobject import ReconnectLDAPObject
from ldap0.lock import LDAPLock

#-----------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------

__all__ = [
    'RESULT_CODE_NAME',
    'RESULT_CODE',
    'LocalLDAPConn',
]

# Number of times connecting to LDAP is retried before sending a failed
# response for a query
LDAP_MAXRETRYCOUNT = 10
# Time to wait before retrying to connect within one query
LDAP_RETRYDELAY = 0.1

# standard cache TTL to be used with LDAPObject
LDAP_CACHETTL = 30.0

# Timeout in seconds when connecting to local and remote LDAP servers
# used for ldap0.OPT_NETWORK_TIMEOUT and ldap0.OPT_TIMEOUT
LDAP_TIMEOUT = 3.0

RESULT_CODE_NAME = {
    0: 'success',
    1: 'operationsError',
    2: 'protocolError',
    3: 'timeLimitExceeded',
    4: 'sizeLimitExceeded',
    5: 'compareFalse',
    6: 'compareTrue',
    7: 'authMethodNotSupported',
    8: 'strongerAuthRequired',
    #     -- 9 reserved --
    10: 'referral',
    11: 'adminLimitExceeded',
    12: 'unavailableCriticalExtension',
    13: 'confidentialityRequired',
    14: 'saslBindInProgress',
    16: 'noSuchAttribute',
    17: 'undefinedAttributeType',
    18: 'inappropriateMatching',
    19: 'constraintViolation',
    20: 'attributeOrValueExists',
    21: 'invalidAttributeSyntax',
    32: 'noSuchObject',
    33: 'aliasProblem',
    34: 'invalidDNSyntax',
    #     -- 35 reserved for undefined isLeaf --
    36: 'aliasDereferencingProblem',
    #     -- 37-47 unused --
    48: 'inappropriateAuthentication',
    49: 'invalidCredentials',
    50: 'insufficientAccessRights',
    51: 'busy',
    52: 'unavailable',
    53: 'unwillingToPerform',
    54: 'loopDetect',
    #     -- 55-63 unused --
    64: 'namingViolation',
    65: 'objectClassViolation',
    66: 'notAllowedOnNonLeaf',
    67: 'notAllowedOnRDN',
    68: 'entryAlreadyExists',
    69: 'objectClassModsProhibited',
    #     -- 70 reserved for CLDAP --
    71: 'affectsMultipleDSAs',
    #     -- 72-79 unused --
    80: 'other',
}

RESULT_CODE = {
    v: k
    for k, v in RESULT_CODE_NAME.items()
}


RESULT_CODE.update({
    ldap0.SUCCESS: 0x00,
    ldap0.OPERATIONS_ERROR: 0x01,
    ldap0.PROTOCOL_ERROR: 0x02,
    ldap0.TIMELIMIT_EXCEEDED: 0x03,
    ldap0.SIZELIMIT_EXCEEDED: 0x04,
    ldap0.COMPARE_FALSE: 0x05,
    ldap0.COMPARE_TRUE: 0x06,
    ldap0.AUTH_METHOD_NOT_SUPPORTED: 0x07,
    ldap0.STRONG_AUTH_REQUIRED: 0x08,
    ldap0.PARTIAL_RESULTS: 0x09,
    ldap0.ADMINLIMIT_EXCEEDED: 0x0b,
    ldap0.CONFIDENTIALITY_REQUIRED: 0x0d,
    ldap0.NO_SUCH_ATTRIBUTE: 0x10,
    ldap0.UNDEFINED_TYPE: 0x11,
    ldap0.INAPPROPRIATE_MATCHING: 0x12,
    ldap0.CONSTRAINT_VIOLATION: 0x13,
    ldap0.TYPE_OR_VALUE_EXISTS: 0x14,
    ldap0.INVALID_SYNTAX: 0x15,
    ldap0.NO_SUCH_OBJECT: 0x20,
    ldap0.ALIAS_PROBLEM: 0x21,
    ldap0.INVALID_DN_SYNTAX: 0x22,
    ldap0.IS_LEAF: 0x23,
    ldap0.ALIAS_DEREF_PROBLEM: 0x24,
    ldap0.X_PROXY_AUTHZ_FAILURE: 0x2F,
    ldap0.INAPPROPRIATE_AUTH: 0x30,
    ldap0.INVALID_CREDENTIALS: 0x31,
    ldap0.INSUFFICIENT_ACCESS: 0x32,
    ldap0.BUSY: 0x33,
    ldap0.UNAVAILABLE: 0x34,
    ldap0.UNWILLING_TO_PERFORM: 0x35,
    ldap0.LOOP_DETECT: 0x36,
    ldap0.NAMING_VIOLATION: 0x40,
    ldap0.OBJECT_CLASS_VIOLATION: 0x41,
    ldap0.NOT_ALLOWED_ON_NONLEAF: 0x42,
    ldap0.NOT_ALLOWED_ON_RDN: 0x43,
    ldap0.ALREADY_EXISTS: 0x44,
    ldap0.NO_OBJECT_CLASS_MODS: 0x45,
    ldap0.RESULTS_TOO_LARGE: 0x46,
    ldap0.AFFECTS_MULTIPLE_DSAS: 0x47,
    ldap0.VLV_ERROR: 0x4C,
    ldap0.OTHER: 0x50,
})


#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------

LDAP_DATETIME_FORMAT = r'%Y%m%d%H%M%SZ'


def ldap_float_str(fln: float) -> str:
    """
    Return fln as string formatted for NumString
    """
    return '%0.5f' % (fln,)


class LocalLDAPConn:
    """
    mix-in class providing a lazily opened local LDAP connection
    """
    ldapi_authz_id = ''
    ldap_retry_max = 4
    ldap_retry_delay = 1.0
    ldap_timeout = LDAP_TIMEOUT
    ldap_cache_ttl = 0.0
    ldap_trace_level = 0

    def __init__(self, logger, ldapi_uri='ldapi://'):
        # Create a fileobj-like logging wrapper instance
        self._logger = logger
        # shadow attribute for property method
        self._ldapi_uri = ldapi_uri
        # For lazy LDAPI connecting in self.get_ldapi_conn()
        self._ldapi_conn = None
        self._ldapi_conn_lock = LDAPLock(
            desc='get_ldapi_conn() in %r' % (self.__class__,)
        )

    @property
    def ldapi_uri(self):
        """
        return LDAPI URI used internally
        """
        return self._ldapi_uri

    @ldapi_uri.setter
    def ldapi_uri(self, ldapi_uri):
        """
        set LDAPI URI used internally, current LDAPI connection is terminated
        """
        if self._ldapi_uri != ldapi_uri:
            self._ldapi_uri = ldapi_uri
            self.disable_ldapi_conn()


    def disable_ldapi_conn(self):
        """
        Destroy local LDAPI connection and reset it to None.
        Should be invoked when catching a ldap0.SERVER_DOWN exception.
        """
        try:
            self._ldapi_conn_lock.acquire()
            if self._ldapi_conn:
                self._ldapi_conn.unbind_s()
        finally:
            # Free it
            del self._ldapi_conn
            # Reset it
            self._ldapi_conn = None
            self._ldapi_conn_lock.release()

    def get_ldapi_conn(self, ldapobj_cls=ReconnectLDAPObject, **kwargs):
        """
        Open a single local LDAPI connection and bind with SASL/EXTERNAL if
        needed
        """
        if isinstance(self._ldapi_conn, ldapobj_cls):
            self._logger.debug(
                'Use existing LDAP connection to %r (%r)',
                self._ldapi_conn.uri,
                self._ldapi_conn,
            )
            return self._ldapi_conn
        # open new LDAPI connection here
        ldapobj_kwargs = dict(
            trace_level=self.ldap_trace_level,
            cache_ttl=self.ldap_cache_ttl,
            retry_max=self.ldap_retry_max,
            retry_delay=self.ldap_retry_delay,
        )
        ldapobj_kwargs.update(kwargs)
        try:
            self._ldapi_conn_lock.acquire()
            try:
                self._ldapi_conn = ldapobj_cls(self.ldapi_uri, **ldapobj_kwargs)
                # Set timeout values
                self._ldapi_conn.set_option(ldap0.OPT_NETWORK_TIMEOUT, self.ldap_timeout)
                self._ldapi_conn.set_option(ldap0.OPT_TIMEOUT, self.ldap_timeout)
                # SASL/EXTERNAL bind
                self._ldapi_conn.sasl_non_interactive_bind_s(
                    'EXTERNAL',
                    authz_id=self.ldapi_authz_id or ''
                )
                authz_id = self._ldapi_conn.whoami_s()
            except ldap0.LDAPError as ldap_error:
                self._ldapi_conn = None
                self._logger.error('LDAPError connecting to %r: %s', self.ldapi_uri, ldap_error)
                raise ldap_error
            else:
                self._logger.info(
                    'Successfully bound to %r as %r (%r)',
                    self.ldapi_uri,
                    authz_id,
                    self._ldapi_conn,
                )
        finally:
            self._ldapi_conn_lock.release()
        return self._ldapi_conn # get_ldapi_conn()
