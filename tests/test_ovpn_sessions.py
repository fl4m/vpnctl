from vpnctl.ovpn.sessions import Session, SessionManager


class MockSession:
    props = {
        "session_name": "test-session",
        "config_name": "test-config",
        "config_path": "/net/mockmock/configs/1337",
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


def test_sm_get_session():
    sm = SessionManager()
    notFound = "/this/wont/work"
    s = sm.get(notFound)
    assert s is None


def test_get_name():
    ovpn_s = MockSession()
    s = Session(ovpn_s)
    assert s.name == "test-session"


def test_get_config():
    ovpn_s = MockSession()
    s = Session(ovpn_s)
    assert s.configuration_path == "/net/mockmock/configs/1337"


def test_get_status():
    ovpn_s = MockSession()
    s = Session(ovpn_s)
    from vpnctl import Status

    assert s.status == Status.CONNECTED
