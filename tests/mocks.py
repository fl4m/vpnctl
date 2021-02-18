import typing

import dbus

from vpnctl.ovpn.wrapper import BaseManager, DBusWrapper


class OvpnObject:
    def __init__(self, path, **props):
        self._path = dbus.ObjectPath(path)
        self._props = props

    def properties(self):
        return self._props.keys()

    def GetPath(self):
        return self._path

    def GetProperty(self, prop):
        return self._props[prop]


class WrapperMixin(DBusWrapper):
    _bus = None

    def _dbus_object(self):
        return None

    def list_properties(self) -> typing.List[str]:
        return self.wrapped.properties


def wrapper_for(cls: typing.Type[DBusWrapper]):
    class MockedWrapper(cls, WrapperMixin):
        pass

    return MockedWrapper


class OvpnManager:
    def __init__(self):
        self._objects: typing.Dict[str, OvpnObject] = dict()

    def add(self, obj: OvpnObject):
        p = str(obj.GetPath())
        self._objects[p] = obj

    def by_property_fetcher(self, prop, cmp=str.startswith):
        def lookup(cmp_value):
            ret = list()
            for path, obj in self._objects.items():
                v = obj.GetProperty(prop)
                if cmp(v, cmp_value):
                    ret.append(path)
            return ret

        return lookup

    def Retrieve(self, path: str):
        return self._objects[path]

    def FetchAvailableObjects(self):
        return self._objects.values()


def get_manager_mixin(manager_instance):
    class MockManagerMixin(BaseManager):
        def __init__(self, obj_cls, mgr):
            super().__init__(wrapper_for(obj_cls), manager_instance)

    return MockManagerMixin


def manager_with(mgr_cls: typing.Type[BaseManager], *objects: OvpnObject):
    """Creates a mocked instance of the given manager type adding all passed
    objects.

    :param mgr_cls: the manager class to inherit from
    :param objects: will be added to the mocked manager
    :returns: a new instance of the mocked manager"""

    manager = OvpnManager()
    for o in objects:
        manager.add(o)

    # Set Lookup method
    from vpnctl.ovpn import ConfigManager

    prop = "name" if mgr_cls is ConfigManager else "config_name"
    manager.LookupConfigName = manager.by_property_fetcher(prop)
    mixin = get_manager_mixin(manager)

    class MockedManager(mgr_cls, mixin):
        pass

    return MockedManager()
