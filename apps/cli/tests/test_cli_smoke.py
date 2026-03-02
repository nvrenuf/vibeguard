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


def test_init_help() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["init", "--help"])
    assert exc.value.code == 0


def test_check_returns_non_zero_when_required_file_missing(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    for file_name in ["README.md", "SECURITY.md", "ARCHITECTURE.md", "AGENTS.md"]:
        (repo / file_name).write_text("ok\n", encoding="utf-8")

    exit_code = main(["check", str(repo), "--policy", "policies/bundles/baseline/policy.yaml"])

    assert exit_code == 1
