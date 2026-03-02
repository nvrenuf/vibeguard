import json
from pathlib import Path

from packages.core.policy_loader import load_policy_bundle
from packages.gates.runner import run_gates

REQUIRED_FILES = ["README.md", "SECURITY.md", "ARCHITECTURE.md", "AGENTS.md", "ISSUE_ORDER.md"]


def _write_required_files(repo: Path) -> None:
    for file_name in REQUIRED_FILES:
        (repo / file_name).write_text("ok\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    workflow_dir = repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "verify.yml").write_text("name: verify\n", encoding="utf-8")


def test_unknown_gate_fails_closed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    policy_path = tmp_path / "policy.json"
    policy_path.write_text(
        json.dumps(
            {
                "id": "test",
                "version": "0.1.0",
                "description": "test",
                "gates": [{"id": "DOES_NOT_EXIST", "enabled": True, "config": {}}],
            },
        ),
        encoding="utf-8",
    )

    report = run_gates(load_policy_bundle(policy_path), repo)

    assert report.summary.overall_status == "fail"
    assert len(report.findings) == 1
    assert report.findings[0].gate_id == "DOES_NOT_EXIST"
    assert report.findings[0].severity == "high"


def test_vg001_passes_when_files_exist(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)

    report = run_gates(load_policy_bundle(Path("policies/bundles/baseline/policy.yaml")), repo)

    assert report.summary.overall_status == "pass"
    assert report.findings == []


def test_vg001_fails_when_required_file_missing(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _write_required_files(repo)
    (repo / "ISSUE_ORDER.md").unlink()

    report = run_gates(load_policy_bundle(Path("policies/bundles/baseline/policy.yaml")), repo)

    assert report.summary.overall_status == "fail"
    assert len(report.findings) == 1
    assert report.findings[0].id == "VG001:ISSUE_ORDER.md"
