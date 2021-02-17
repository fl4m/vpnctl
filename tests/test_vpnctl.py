import pytest
from click.testing import CliRunner

from vpnctl import commands
from vpnctl import __version__


def test_version():
    """Should print the version information."""

    runner = CliRunner()
    result = runner.invoke(commands.cli, ["--version"])

    assert __version__ in result.output


@pytest.mark.parametrize(
    "cli", ["--version", "--help", "status", "list", "clear"]
)
def test_command_exit_success(cli):
    runner = CliRunner()
    result = runner.invoke(commands.cli, [cli])

    assert result.exit_code == 0
