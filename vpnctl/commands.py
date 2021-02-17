from functools import wraps

import click
from tabulate import tabulate

from . import Status, __version__


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


@click.option("--verbose/--short", "-v/", default=False)
@cli.command()
@with_ovpn_import
def status(verbose):
    """Get the current VPN status."""

    from .ovpn import ConfigManager, SessionManager

    sm = SessionManager()
    cm = ConfigManager()
    sessions = sm.get_all()
    lines = list()

    for s in sessions:
        c = cm.get(s.configuration_path)
        line, n = None, ""
        if c is not None:
            n = c.name
        else:
            n = s.name + " (temporary connection)"
        if s.status == Status.CONNECTED:
            line = f"Connected to {n}."
        if verbose:
            color = "green" if s.status == Status.CONNECTED else "red"
            line = [
                s.id,
                click.style(str(s.status), fg=color),
                n,
                s.created.ctime(),
            ]

        if line is not None:
            lines.append(line)

    if len(lines) > 0:
        if verbose:
            headers = ["ID", "Status", "Connection", "Created"]
            click.echo(tabulate(lines, headers=headers))
        else:
            click.echo("\n".join(lines))
    else:
        click.echo(Status.DISCONNECTED)
