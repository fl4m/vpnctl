import vpnctl
from vpnctl import __version__


def test_version():
    assert __version__ == "0.0.1"


def test_main(capsys):
    """Should print the version information."""
    vpnctl.main()
    captured = capsys.readouterr()
    assert captured.out == f"vpnctl v0.0.1\n"
