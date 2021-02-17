from datetime import datetime

from vpnctl import Status
from vpnctl.ovpn.sessions import Session, SessionManager


TIMESTAMP = datetime.now()


class MockSession:
    props = {
        "session_name": "test-session",
        "config_name": "test-config",
        "config_path": "/net/mockmock/configs/1337",
        "session_created": int(TIMESTAMP.timestamp()),
    }

    def GetProperty(self, k):
        return self.props[k]

    def GetStatus(self):
        from vpnctl.ovpn.vendor.openvpn3 import StatusMajor, StatusMinor

        return {
            "major": StatusMajor.CONNECTION,
            "minor": StatusMinor.CONN_CONNECTED,
            "message": "",
        }


def test_get_properties():
    ovpn_s = MockSession()
    s = Session(ovpn_s)

    assert s.name == "test-session"
    assert s.configuration_path == "/net/mockmock/configs/1337"
    assert s.status == Status.CONNECTED
    assert s.created == TIMESTAMP.replace(microsecond=0)


def test_sm_get_session_not_found():
    sm = SessionManager()
    notFound = "/this/wont/work"
    s = sm.get(notFound)
    assert s is None
