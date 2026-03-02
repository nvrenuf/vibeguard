import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from packages.core.policy_loader import load_policy_bundle
from packages.gates.runner import run_gates
from packages.reporting.audit_pack import create_audit_pack

from vibeguard_cli.main import main

POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")


def _write_required_files(repo: Path) -> None:
    for file_name in ["README.md", "SECURITY.md", "ARCHITECTURE.md", "AGENTS.md", "ISSUE_ORDER.md"]:
        (repo / file_name).write_text("ok\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    workflow_dir = repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "verify.yml").write_text("name: verify\n", encoding="utf-8")


def _run_report(repo: Path):
    policy_bundle = load_policy_bundle(POLICY_PATH)
    return run_gates(policy=policy_bundle, repo_path=repo)


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def test_audit_pack_structure_created(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    report = _run_report(repo)
    out_dir = tmp_path / "audit-pack"
    run_dir = create_audit_pack(
        repo_path=repo,
        policy_path=POLICY_PATH,
        findings_report=report,
        out_dir=out_dir,
        run_id="20260302T052130Z-testsha",
        created_at=datetime(2026, 3, 2, 5, 21, 30, tzinfo=timezone.utc),  # noqa: UP017
    )

    assert run_dir == out_dir / "20260302T052130Z-testsha"
    assert (run_dir / "manifest.json").is_file()
    assert (run_dir / "reports" / "findings.json").is_file()
    assert (run_dir / "reports" / "summary.md").is_file()
    assert (run_dir / "policy_bundle" / "policy.yaml").is_file()
    assert (run_dir / "evidence").is_dir()


def test_manifest_fields_and_hashes(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    report = _run_report(repo)
    run_dir = create_audit_pack(
        repo_path=repo,
        policy_path=POLICY_PATH,
        findings_report=report,
        out_dir=tmp_path / "audit-pack",
        run_id="20260302T052130Z-fixed",
        created_at=datetime(2026, 3, 2, 5, 21, 30, tzinfo=timezone.utc),  # noqa: UP017
    )

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_id"] == "20260302T052130Z-fixed"
    assert manifest["repo_path"] == str(repo)
    assert manifest["policy_path"] == str(POLICY_PATH)
    assert manifest["python_version"]
    assert manifest["platform"]
    assert manifest["os"]

    file_entries = manifest["files"]
    paths = [item["path"] for item in file_entries]
    assert paths == sorted(paths)

    entries_by_path = {item["path"]: item for item in file_entries}
    findings_bytes = (run_dir / "reports" / "findings.json").read_bytes()
    policy_bytes = (run_dir / "policy_bundle" / "policy.yaml").read_bytes()

    assert entries_by_path["reports/findings.json"]["sha256"] == _sha256(findings_bytes)
    assert entries_by_path["reports/findings.json"]["size_bytes"] == len(findings_bytes)
    assert entries_by_path["policy_bundle/policy.yaml"]["sha256"] == _sha256(policy_bytes)
    assert entries_by_path["policy_bundle/policy.yaml"]["size_bytes"] == len(policy_bytes)


def test_policy_snapshot_matches_input_policy(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    report = _run_report(repo)
    run_dir = create_audit_pack(
        repo_path=repo,
        policy_path=POLICY_PATH,
        findings_report=report,
        out_dir=tmp_path / "audit-pack",
        run_id="20260302T052130Z-policy",
        created_at=datetime(2026, 3, 2, 5, 21, 30, tzinfo=timezone.utc),  # noqa: UP017
    )

    snapshot = (run_dir / "policy_bundle" / "policy.yaml").read_text(encoding="utf-8")
    assert snapshot == POLICY_PATH.read_text(encoding="utf-8")


def test_cli_writes_pack_even_when_failing(tmp_path: Path, capsys) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    out_dir = tmp_path / "audit-pack"
    exit_code = main(
        ["audit-pack", str(repo), "--policy", str(POLICY_PATH), "--out-dir", str(out_dir)],
    )
    assert exit_code != 0

    printed_path = capsys.readouterr().out.strip()
    run_dir = Path(printed_path)
    assert run_dir.exists()

    findings = json.loads((run_dir / "reports" / "findings.json").read_text(encoding="utf-8"))
    assert findings["summary"]["overall_status"] == "fail"
    assert (run_dir / "reports" / "summary.md").is_file()
