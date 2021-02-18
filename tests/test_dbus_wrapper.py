import dbus

from vpnctl.ovpn.wrapper import DBusWrapper
from . import mocks


class SampleWrapper(DBusWrapper):
    _interface_name = "org.freedesktop.DBus"
    _bus = dbus.SystemBus()

    def __init__(self, path):
        super().__init__(mocks.OvpnObject(path))

    def _get_property(self, name: str):
        props_if = "org.freedesktop.DBus.Properties"
        props = dbus.Interface(self._dbus_object, props_if)
        return props.Get(self._interface_name, name)


existing_path = "/org/freedesktop/DBus"
nonexisting_path = "/this/wont/work"


def test_exists():
    w = SampleWrapper(existing_path)
    assert w.exists()


def test_not_exists():
    w = SampleWrapper(nonexisting_path)
    assert not w.exists()


def test_list_properties():
    w = SampleWrapper(existing_path)
    expected = ["Features", "Interfaces"]
    result = w.list_properties()

    assert len(result) == len(expected)
    assert all([a == b for a, b in zip(result, expected)])


def test_get_property():
    w = SampleWrapper(existing_path)
    expected = "org.freedesktop.DBus.Monitoring"

    assert expected in w._get_property("Interfaces")


def test_get_id():
    w = SampleWrapper(existing_path)
    assert w.id == "DBus"
