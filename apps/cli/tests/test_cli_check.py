import json
from pathlib import Path

from packages.reporting.findings import Finding, FindingsReport

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


def test_check_fail_on_threshold_controls_exit_code(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    mocked_report = FindingsReport.create(
        repo=str(repo),
        policy_id="baseline",
        policy_version="0.1.0",
        findings=[
            Finding(
                id="F-1",
                gate_id="VG001",
                severity="medium",
                title="Medium issue",
                message="x",
            ),
        ],
    )

    monkeypatch.setattr("vibeguard_cli.main.run_gates", lambda policy, repo_path: mocked_report)

    assert run_check(repo, Path("policies/bundles/baseline/policy.yaml"), fail_on="high") == 0
    assert run_check(repo, Path("policies/bundles/baseline/policy.yaml"), fail_on="medium") == 1
    assert run_check(repo, Path("policies/bundles/baseline/policy.yaml"), fail_on="low") == 1


def test_check_sarif_output_has_required_top_level_keys(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)
    out = tmp_path / "result.sarif"

    mocked_report = FindingsReport.create(
        repo=str(repo),
        policy_id="baseline",
        policy_version="0.1.0",
        findings=[
            Finding(
                id="F-1",
                gate_id="VG001",
                severity="high",
                title="Missing file",
                message="x",
                path="README.md",
                line=1,
            ),
            Finding(
                id="F-2",
                gate_id="VG002",
                severity="medium",
                title="Forbidden path",
                message="y",
            ),
        ],
    )
    monkeypatch.setattr("vibeguard_cli.main.run_gates", lambda policy, repo_path: mocked_report)

    exit_code = run_check(
        repo,
        Path("policies/bundles/baseline/policy.yaml"),
        out=out,
        output_format="sarif",
        fail_on="high",
    )
    assert exit_code == 1

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["version"] == "2.1.0"
    assert "$schema" in payload
    assert "runs" in payload
    assert payload["runs"][0]["tool"]["driver"]["name"] == "vibeguard"
    assert len(payload["runs"][0]["results"]) == 2
