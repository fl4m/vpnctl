from functools import wraps

import click
from . import __version__, Status


@click.version_option(__version__)
@click.group()
def cli():
    """A command-line utility to interact with VPN systems."""

    pass


def with_ovpn_import(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ModuleNotFoundError:
            raise click.ClickException("The OpenVPN backend was not found.")

    return wrapper


@cli.command("list")
@with_ovpn_import
def list_cfgs():
    """List available VPN configurations."""

    from .ovpn import ConfigManager

    m = ConfigManager()
    for c_name in m.list_configurations():
        click.echo(c_name)


@cli.command()
@with_ovpn_import
def status():
    """Get the current VPN status."""

    from .ovpn import SessionManager

    m = SessionManager()
    for s in m.list_sessions():
        click.echo(s.get_status())
    else:
        click.echo(Status.DISCONNECTED)
