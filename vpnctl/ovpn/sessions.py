from datetime import datetime

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
        s = self.wrapped.GetStatus()

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

    @property
    def created(self):
        """Date and Time when this session was created."""
        return datetime.fromtimestamp(self._get_property("session_created"))

    def connect(self):
        """Initialize and start this session."""
        pass

    def disconnect(self):
        """Stop and delete this session."""
        self.wrapped.Disconnect()


class SessionManager(OvpnManager[Session]):
    def __init__(self):
        super().__init__(Session, openvpn3.SessionManager(OVPN_BUS))

    def clearer(self):
        """Clear unused session via a generator.

        :returns: a tuple consisting of the number of sessions to delete
        and a generator which will delete the sessions one at a time to enable
        some form of updates."""
        to_delete = list()
        for s in self.get_all():
            if s.status == Status.DISCONNECTED:
                to_delete.append(s)

        def generator():
            for s in to_delete:
                id = s.id
                s.disconnect()
                yield id

        return len(to_delete), generator()

    def clear(self):
        """Remove all unused (disconnected) sessions and return their names."""

        _, gen = self.clearer()
        return list(gen())
