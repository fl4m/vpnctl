import dbus
import openvpn3


class OpenVPNManager:
    def __init__(self):
        self.config_mgr = openvpn3.ConfigurationManager(dbus.SystemBus())

    def list_configurations(self):
        cfgs = self.config_mgr.FetchAvailableConfigs()
        return [str(c.GetProperty("name")) for c in cfgs]


def list_configuration_properties(config):
    config = dbus.SystemBus().get_object(
        "net.openvpn.v3.configuration", config.GetPath()
    )
    prop_intf = dbus.Interface(config, dbus_interface="org.freedesktop.DBus.Properties")
    return prop_intf.GetAll("net.openvpn.v3.configuration")
