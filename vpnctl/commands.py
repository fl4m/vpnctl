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
    for c in m.get_all():
        click.echo(c.name)


@cli.command()
@with_ovpn_import
def status():
    """Get the current VPN status."""

    from .ovpn import ConfigManager, SessionManager

    sm = SessionManager()
    cm = ConfigManager()
    sessions = sm.get_all()
    for s in sessions:
        c = cm.get(s.configuration_path)
        if c is not None:
            click.echo(f"{c.name}: {s.status}\n")
        else:
            click.echo(f"{s.name}: {s.status} (temporary configuration)\n")
    if len(sessions) == 0:
        click.echo(Status.DISCONNECTED)
