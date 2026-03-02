from typer.testing import CliRunner

from vibeguard_cli.main import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "VibeGuard" in result.stdout or "vibeguard" in result.stdout.lower()
