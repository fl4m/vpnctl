from .vendor import openvpn3
from . import OVPN_BUS


class ConfigManager:
    def __init__(self):
        self.config_mgr = openvpn3.ConfigurationManager(OVPN_BUS)

    def list_configurations(self):
        cfgs = self.config_mgr.FetchAvailableConfigs()
        return [str(c.GetProperty("name")) for c in cfgs]

    def get_config(self, path):
        """Get a configuration via its dbus object path."""
        self.config_mgr.Retrieve(path)
