__version__ = "0.0.1"

import dbus
from enum import Enum, auto

OVPN_BUS = dbus.SystemBus()


class Status(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    PAUSED = auto()

    def __str__(self):
        return self.name.lower()
