import click
from . import __version__


@click.version_option(__version__)
@click.group()
def cli():
    """A command-line utility to interact with VPN systems."""

    pass


@cli.command("list")
def list_cfgs():
    """List available VPN configurations."""

    try:
        from .ovpn import OpenVPNManager
        m = OpenVPNManager()
        for c_name in m.list_configurations():
            click.echo(c_name)
    except ModuleNotFoundError:
        click.echo("The OpenVPN backend was not found.")