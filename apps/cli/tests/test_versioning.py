import json
from datetime import datetime, timezone
from pathlib import Path

from packages.core.policy_loader import load_policy_bundle
from packages.gates.runner import run_gates
from packages.reporting.audit_pack import create_audit_pack
from packages.reporting.findings import FindingsReport
from typer.testing import CliRunner

from vibeguard_cli.main import app

POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")


runner = CliRunner()


def _write_required_files(repo: Path) -> None:
    for file_name in ["README.md", "SECURITY.md", "ARCHITECTURE.md", "AGENTS.md", "ISSUE_ORDER.md"]:
        (repo / file_name).write_text("ok\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    workflow_dir = repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "verify.yml").write_text("name: verify\n", encoding="utf-8")


def test_version_cli() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_findings_includes_version() -> None:
    report = FindingsReport.create(
        repo=".",
        policy_id="baseline",
        policy_version="0.1.0",
        generated_at="2026-01-01T00:00:00+00:00",
        findings=[],
        vibeguard_version="0.1.0",
    )

    payload = json.loads(report.to_json())
    assert payload["run"]["vibeguard_version"] == "0.1.0"


def test_audit_pack_manifest_includes_version(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    policy_bundle = load_policy_bundle(POLICY_PATH)
    report = run_gates(policy=policy_bundle, repo_path=repo)
    run_dir = create_audit_pack(
        repo_path=repo,
        policy_path=POLICY_PATH,
        findings_report=report,
        out_dir=tmp_path / "audit-pack",
        run_id="20260302T052130Z-version",
        created_at=datetime(2026, 3, 2, 5, 21, 30, tzinfo=timezone.utc),  # noqa: UP017
    )

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["vibeguard_version"] == "0.1.0"
