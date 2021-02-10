from click.testing import CliRunner

from vpnctl import commands
from vpnctl import __version__


def test_version():
    """Should print the version information."""

    runner = CliRunner()
    result = runner.invoke(commands.cli, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_status():
    runner = CliRunner()
    result = runner.invoke(commands.cli, ["status"])

    assert result.exit_code == 0
