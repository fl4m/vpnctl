from .vendor import openvpn3

from .. import Status
from . import OVPN_BUS


class Session:
    """Wraps a OpenVPN session."""

    def __init__(self, ovpn_session: openvpn3.Session):
        self.ovpn_session = ovpn_session

    def get_status(self) -> Status:
        # retrieve status object
        s = self.ovpn_session.GetStatus()

        # handle other cases
        if s["major"] != openvpn3.StatusMajor.CONNECTION:
            return Status.DISCONNECTED

        # mapping
        status_map = {
            openvpn3.StatusMinor.CONN_CONNECTED: Status.CONNECTED,
            openvpn3.StatusMinor.CONN_PAUSED: Status.PAUSED,
        }

        # return with default
        return status_map.get(s["minor"], Status.DISCONNECTED)

    def get_path(self):
        return self.ovpn_session.GetPath()

    def get_config_path(self):
        return self.ovpn_session.GetProperty("config_path")


class SessionManager:
    def __init__(self):
        self.session_mgr = openvpn3.SessionManager(OVPN_BUS)

    def list_sessions(self):
        sessions = self.session_mgr.FetchAvailableSessions()
        return [Session(s) for s in sessions]
