from pathlib import Path

import pytest

from vibeguard_cli.main import main, run_init


def test_init_creates_expected_structure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target = tmp_path / "project"

    exit_code = main(["init", str(target)])
    assert exit_code == 0

    assert (target / "policies/bundles/baseline/policy.yaml").is_file()
    assert (target / "out/audit-pack").is_dir()
    assert (target / "out/findings").is_dir()
    assert (target / "evidence").is_dir()

    output = capsys.readouterr().out
    assert "Initialized VibeGuard project:" in output


def test_init_refuses_overwrite_without_force(tmp_path: Path) -> None:
    target = tmp_path / "project"
    target.mkdir(parents=True, exist_ok=True)
    policy = target / "policies/bundles/baseline/policy.yaml"
    policy.parent.mkdir(parents=True, exist_ok=True)
    policy.write_text("custom-policy\n", encoding="utf-8")

    with pytest.raises(ValueError):
        run_init(target, force=False)

    run_init(target, force=True)
    assert "custom-policy\n" != policy.read_text(encoding="utf-8")
