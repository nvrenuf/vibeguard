import pytest

from vibeguard_cli.main import main


def test_help() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_check_help() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["check", "--help"])
    assert exc.value.code == 0


def test_audit_pack_help() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["audit-pack", "--help"])
    assert exc.value.code == 0
