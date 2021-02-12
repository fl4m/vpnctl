import dbus

from vpnctl.ovpn.wrapper import DBusWrapper


class TestWrapper(DBusWrapper):
    _interface_name = "org.freedesktop.DBus"
    _bus = dbus.SessionBus()

    def __init__(self, path):
        dbo = self._bus.get_object(self._interface_name, path)
        super().__init__(dbo)


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
