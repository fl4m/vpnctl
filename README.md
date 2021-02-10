# vpnctl

A simple command line interface for managing and controlling VPN connections.

## Goals

This project strives to simplify interaction with VPN tools through the command
line. It will first support OpenVPN connections but may be expanded later.
Its primary focus is on Unix and Mac users.

## Requirements

The first backend implemented is OpenVPN3. It must be installed through your
distribution's package manager.

## Development

Because the openvpn3 python module is not separately packaged we decided to
vendor it for the time until it reaches a stable version.

It also requires the python-dbus library which in is available through PyPI
but requires the following libraries to be installed. Their names may be
different on your platform:

* python3-devel
* dbus-devel
* glib2-devel

* * *

&copy; 2021 Robert Mörseburg &ndash;
Licensed under the [MIT License](./LICENSE).
