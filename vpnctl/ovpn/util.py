import dbus
from .. import OVPN_BUS


def get_all_properties(interface, path):
    """Returns a List of all the object's properties."""
    obj = OVPN_BUS.get_object(interface, path)
    props = dbus.Interface(obj, "org.freedesktop.DBus.Properties")
    return props.GetAll(interface)
