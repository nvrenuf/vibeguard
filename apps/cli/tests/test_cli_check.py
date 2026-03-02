import json
from pathlib import Path

from vibeguard_cli.main import run_check


def _write_required_files(repo: Path) -> None:
    for file_name in ["README.md", "SECURITY.md", "ARCHITECTURE.md", "AGENTS.md", "ISSUE_ORDER.md"]:
        (repo / file_name).write_text("ok\n", encoding="utf-8")


def test_check_outputs_findings_json(tmp_path: Path, capsys) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    exit_code = run_check(repo, Path("policies/bundles/baseline/policy.yaml"))

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "1.0"
    assert payload["run"]["policy_id"] == "baseline"
    assert payload["summary"]["overall_status"] == "pass"
    assert payload["findings"] == []


def test_audit_pack_writes_policy_snapshot(tmp_path: Path) -> None:
    from vibeguard_cli.main import run_audit_pack

    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    out_dir = tmp_path / "audit"
    exit_code = run_audit_pack(repo, Path("policies/bundles/baseline/policy.yaml"), out_dir=out_dir)

    assert exit_code == 0
    assert (out_dir / "reports" / "findings.json").is_file()
    assert (out_dir / "policy_bundle" / "policy.yaml").is_file()
