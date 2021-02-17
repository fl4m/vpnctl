from .wrapper import DBusWrapper, OvpnManager
from .vendor import openvpn3
from . import OVPN_BUS


class Configuration(DBusWrapper):
    """Wraps an OpenVPN configuration"""

    _interface_name = "net.openvpn.v3.configuration"

    @property
    def name(self):
        """Name of this Configuration as defined by OpenVPN."""
        return self._get_property("name")


class ConfigManager(OvpnManager[Configuration]):
    """Contains all methods to create and retrieve OpenVPN configurations."""

    def __init__(self):
        super().__init__(Configuration, openvpn3.ConfigurationManager(OVPN_BUS))

    def get_by_name(self, name):
        """Lookup a persistent configuration by its name."""

        # returns a list of matching DBus paths
        cfgs = self.mgr_instance.LookupConfigName(name)

        if len(cfgs) > 1:
            raise ValueError("There were multiple configurations found.")
        if len(cfgs) == 0:
            return None
        return self.get(cfgs[0])
