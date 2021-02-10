#
# Generated by ../../src/python/openvpn3/gen-python-constants
# as part of the project build.
#
# This file is part of openvpn3-linux, licensed
# under AGPLv3.  Please see the main COPYRIGHT.md
# file packaged with the project for more details.
#
# Do not modify this file.  This file needs to be
# regenerated each time any of the OpenVPN 3 Linux
# constants are modified.
#

from enum import Enum, IntFlag

VERSION = 'v13_beta'

class StatusMajor(Enum):
    UNSET = 0
    CFG_ERROR = 1
    CONNECTION = 2
    SESSION = 3
    PKCS11 = 4
    PROCESS = 5


class StatusMinor(Enum):
    UNSET = 0
    CFG_ERROR = 1
    CFG_OK = 2
    CFG_INLINE_MISSING = 3
    CFG_REQUIRE_USER = 4
    CONN_INIT = 5
    CONN_CONNECTING = 6
    CONN_CONNECTED = 7
    CONN_DISCONNECTING = 8
    CONN_DISCONNECTED = 9
    CONN_FAILED = 10
    CONN_AUTH_FAILED = 11
    CONN_RECONNECTING = 12
    CONN_PAUSING = 13
    CONN_PAUSED = 14
    CONN_RESUMING = 15
    CONN_DONE = 16
    SESS_NEW = 17
    SESS_BACKEND_COMPLETED = 18
    SESS_REMOVED = 19
    SESS_AUTH_USERPASS = 20
    SESS_AUTH_CHALLENGE = 21
    SESS_AUTH_URL = 22
    PKCS11_SIGN = 23
    PKCS11_ENCRYPT = 24
    PKCS11_DECRYPT = 25
    PKCS11_VERIFY = 26
    PROC_STARTED = 27
    PROC_STOPPED = 28
    PROC_KILLED = 29


class ClientAttentionType(Enum):
    UNSET = 0
    CREDENTIALS = 1
    PKCS11 = 2
    ACCESS_PERM = 3


class ClientAttentionGroup(Enum):
    UNSET = 0
    USER_PASSWORD = 1
    PK_PASSPHRASE = 2
    CHALLENGE_STATIC = 3
    CHALLENGE_DYNAMIC = 4
    PKCS11_SIGN = 5
    PKCS11_DECRYPT = 6
    OPEN_URL = 7


class NetCfgChangeType(IntFlag):
    UNSET = 0
    DEVICE_ADDED = 1
    DEVICE_REMOVED = 2
    IPADDR_ADDED = 4
    IPADDR_REMOVED = 8
    ROUTE_ADDED = 16
    ROUTE_REMOVED = 32
    ROUTE_EXCLUDED = 64
    DNS_SERVER_ADDED = 128
    DNS_SERVER_REMOVED = 256
    DNS_SEARCH_ADDED = 512
    DNS_SEARCH_REMOVED = 1024