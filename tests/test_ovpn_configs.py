import pytest

from vpnctl.ovpn import ConfigManager
from . import mocks


def test_get_by_name():
    expected_name = "test-name"
    expected_path = "/test/path/1"

    obj = mocks.OvpnObject(expected_path, name=expected_name)

    cm = mocks.manager_with(ConfigManager, obj)
    c = cm.get_by_name(expected_name)

    assert c.exists()
    assert c.name == expected_name
    assert c._dbus_path == expected_path


def test_get_by_name_none():
    cm = mocks.manager_with(ConfigManager)
    c = cm.get_by_name("wont-work")

    assert c is None


def test_get_by_name_error():
    expected_name = "test-name"
    expected_path = "/test/path/%d"
    objects = (
        mocks.OvpnObject(expected_path % 1, name=expected_name),
        mocks.OvpnObject(expected_path % 2, name=expected_name),
    )

    cm = mocks.manager_with(ConfigManager, *objects)
    with pytest.raises(ValueError, match="multiple"):
        cm.get_by_name(expected_name)
