__version__ = "0.0.1"

from enum import Enum, auto


class Status(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    PAUSED = auto()

    def __str__(self):
        return self.name.lower()
