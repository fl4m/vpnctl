import dbus

from vpnctl.ovpn.wrapper import DBusWrapper
from . import mocks


class TestWrapper(DBusWrapper):
    _interface_name = "org.freedesktop.DBus"
    _bus = dbus.SystemBus()

    def __init__(self, path):
        super().__init__(mocks.OvpnObject(path))


existing_path = "/org/freedesktop/DBus"
nonexisting_path = "/this/wont/work"


def test_exists():
    w = TestWrapper(existing_path)
    assert w.exists()


def test_not_exists():
    w = TestWrapper(nonexisting_path)
    assert not w.exists()


def test_list_properties():
    w = TestWrapper(existing_path)
    expected = ["Features", "Interfaces"]
    result = w.list_properties()

    assert len(result) == len(expected)
    assert all([a == b for a, b in zip(result, expected)])


def test_get_id():
    w = TestWrapper(existing_path)
    assert w.id == "DBus"
