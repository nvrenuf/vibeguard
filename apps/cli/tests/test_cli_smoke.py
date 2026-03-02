from typer.testing import CliRunner

from vibeguard_cli.main import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert result.exception is None
    assert "VibeGuard" in result.stdout or "vibeguard" in result.stdout.lower()


def test_check_help():
    result = runner.invoke(app, ["check", "--help"])
    assert result.exit_code == 0
    assert result.exception is None
    assert "check" in result.stdout.lower()


def test_audit_pack_help():
    result = runner.invoke(app, ["audit-pack", "--help"])
    assert result.exit_code == 0
    assert result.exception is None
    assert "audit-pack" in result.stdout.lower()
