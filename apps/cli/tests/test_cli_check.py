import json
from pathlib import Path

from vibeguard_cli.main import run_check


def _write_required_files(repo: Path) -> None:
    for file_name in ["README.md", "SECURITY.md", "ARCHITECTURE.md", "AGENTS.md", "ISSUE_ORDER.md"]:
        (repo / file_name).write_text("ok\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    workflow_dir = repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "verify.yml").write_text("name: verify\n", encoding="utf-8")


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

