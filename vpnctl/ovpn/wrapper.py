import typing

import dbus

from . import OVPN_BUS


class DBusWrapper:
    _interface_name: str = None
    _bus = OVPN_BUS

    def __init__(self, wrapped):
        if wrapped is None:
            raise ValueError("Cannot wrap None.")
        self._wrapped = wrapped

    @property
    def _dbus_path(self) -> dbus.ObjectPath:
        """Returns the dbus path of the wrapped object."""
        return self.wrapped.GetPath()

    @property
    def _dbus_object(self):
        """Return the dbus object for the wrapped object."""
        return self._bus.get_object(self._interface_name, self._dbus_path)

    @property
    def wrapped(self):
        """Return the wrapped object."""
        return self._wrapped

    @property
    def id(self) -> str:
        """Return the UID given to the wrapped object by OpenVPN."""
        from os.path import basename

        return basename(self._dbus_path)

    def _ping(self):
        """Uses a standard method to check if the specified object exists.

        Defaults to `org.freedesktop.DBus.Properties.GetAll` but may be
        overwritten by subclasses. Note that `org.freedesktop.DBus.Peer.Ping`
        doesn't check the object path."""

        self.list_properties()

    def exists(self):
        """Checks whether the wrapped DBus object can be pinged."""
        try:
            self._ping()
            return True
        except dbus.DBusException as e:
            return False

    def list_properties(self) -> typing.List[str]:
        """Returns a List of all the object's properties."""
        props = dbus.Interface(
            self._dbus_object, "org.freedesktop.DBus.Properties"
        )
        return props.GetAll(self._interface_name)

    def _get_property(self, name: str):
        return self.wrapped.GetProperty(name)


ObjType = typing.TypeVar("ObjType", bound=DBusWrapper)


class BaseManager(typing.Generic[ObjType]):
    """Base class for managing OpenVPN objects."""

    def __init__(self, obj_cls: typing.Type[DBusWrapper], manager):
        """Create a new manager.

        :param manager: the wrapped manager instance
        :param obj_cls: the class of the managed objects"""
        self.mgr_instance = manager
        self._obj_cls = obj_cls

    def get_all(self) -> typing.List[ObjType]:
        return [self._obj_cls(obj) for obj in self._mgr_fetch_all()]

    def _mgr_fetch_all(self):
        methods = [
            getattr(self.mgr_instance, a)
            for a in dir(self.mgr_instance)
            if a.startswith("FetchAvailable")
        ]

        if len(methods) != 1:
            raise AttributeError(
                "Could not determine the 'FetchAll' method. Try overriding it."
            )
        return methods[0]()

    def get(self, path) -> typing.Optional[ObjType]:
        """Create an instance of the class from its DBus path.

        Returns None if there is no object at this path."""

        # Retrieve the object at path
        dbo = self.mgr_instance.Retrieve(path)
        # Create wrapped instance
        obj = self._obj_cls(dbo)

        # check if it really exists
        if obj.exists():
            return obj
        else:
            return None
