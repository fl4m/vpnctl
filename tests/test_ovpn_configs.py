import pytest

from vpnctl.ovpn import ConfigManager
from vpnctl.ovpn.configs import Configuration


class MockConfigObject:
    def __init__(self, name, path):
        self._name = name
        self._path = path

    def GetPath(self):
        return self._path

    def GetProperty(self, prop):
        if prop == "name":
            return self._name
        return None


class MockManager:
    def __init__(self, names):
        self._names = names

    def LookupConfigName(self, name):
        return [v for k, v in self._names if k == name]

    def Retrieve(self, path):
        names = [k for k, v in self._names if v == path]
        if len(names) == 1:
            return MockConfigObject(names[0], path)
        raise RuntimeError("No object at given path.")


class MockConfig(Configuration):
    def list_properties(self):
        return ["name"]


def test_get_by_name():
    expected_name = "test-name"
    expected_path = "test/path/1"

    mock = MockManager([(expected_name, expected_path)])
    ConfigManager._mgr_instance = mock
    ConfigManager._obj_cls = MockConfig

    cm = ConfigManager()
    c = cm.get_by_name(expected_name)

    assert c.exists()
    assert c.name == expected_name
    assert c._dbus_path == expected_path


def test_get_by_name_none():
    ConfigManager._mgr_instance = MockManager([])
    ConfigManager._obj_cls = MockConfig

    cm = ConfigManager()
    c = cm.get_by_name("wont-work")

    assert c is None


def test_get_by_name_error():
    expected_name = "test-name"
    expected_path = "/test/path/%d"
    ConfigManager._mgr_instance = MockManager(
        [
            (expected_name, expected_path % 1),
            (expected_name, expected_path % 2),
        ]
    )
    ConfigManager._obj_cls = MockConfig
    cm = ConfigManager()

    with pytest.raises(ValueError, match="multiple"):
        cm.get_by_name(expected_name)
