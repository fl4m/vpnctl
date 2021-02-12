from .configs import ConfigManager, Configuration
from .wrapper import DBusWrapper, OvpnManager
from .vendor import openvpn3

from .. import Status
from . import OVPN_BUS


class Session(DBusWrapper):
    """Wraps an OpenVPN session."""

    _interface_name = "net.openvpn.v3.sessions"

    # Properties
    @property
    def status(self) -> Status:
        """Connection status of this Session."""

        # retrieve status object
        s = self._wrapped.GetStatus()

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

    @property
    def configuration_path(self):
        """"DBus path of the Configuration associated with this session."""
        return self._get_property("config_path")

    @property
    def name(self):
        """Name of this Session as defined by OpenVPN."""
        return self._get_property("session_name")


class SessionManager(OvpnManager[Session]):
    _obj_cls = Session
    _mgr_instance = openvpn3.SessionManager(OVPN_BUS)
