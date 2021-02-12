from .wrapper import DBusWrapper, OvpnManager
from .vendor import openvpn3
from . import OVPN_BUS


class Configuration(DBusWrapper):
    """Wraps an OpenVPN configuration"""

    _interface_name = "net.openvpn.v3.configuration"

    @property
    def name(self):
        """Name of this Configuration as defined by OpenVPN"""
        return self._get_property("name")


class ConfigManager(OvpnManager[Configuration]):
    """Contains all methods to create and retrieve OpenVPN configurations."""

    _obj_cls = Configuration
    _mgr_instance = openvpn3.ConfigurationManager(OVPN_BUS)
