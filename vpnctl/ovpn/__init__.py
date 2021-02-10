import dbus

OVPN_BUS = dbus.SystemBus()

from .configs import ConfigManager
from .sessions import SessionManager
