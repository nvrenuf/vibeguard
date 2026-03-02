import json
from pathlib import Path

from packages.core.policy_loader import load_policy_bundle
from packages.gates.runner import run_gates


def _policy(tmp_path: Path, gates: list[dict]) -> Path:
    payload = {
        "id": "test",
        "version": "0.1.0",
        "description": "test",
        "gates": gates,
    }
    path = tmp_path / "policy.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_vg004_passes_when_license_exists(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    policy = _policy(tmp_path, [{"id": "VG004", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg004_fails_when_license_missing_and_required(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    policy = _policy(tmp_path, [{"id": "VG004", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "fail"
    assert [finding.id for finding in report.findings] == ["VG004:license"]


def test_vg004_passes_when_notices_missing_but_not_required(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    policy = _policy(tmp_path, [{"id": "VG004", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg004_fails_when_notices_required_and_missing(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG004",
                "enabled": True,
                "config": {"require_third_party_notices": True},
            }
        ],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "fail"
    assert [finding.id for finding in report.findings] == ["VG004:third-party-notices"]


def test_vg004_findings_order_is_deterministic(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG004",
                "enabled": True,
                "config": {
                    "require_license": True,
                    "require_third_party_notices": True,
                },
            }
        ],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert [finding.id for finding in report.findings] == [
        "VG004:license",
        "VG004:third-party-notices",
    ]


def test_vg005_passes_when_verify_workflow_exists(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    workflow_dir = repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True)
    (workflow_dir / "verify.yml").write_text("name: verify\n", encoding="utf-8")
    policy = _policy(tmp_path, [{"id": "VG005", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg005_fails_when_required_workflow_missing(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    policy = _policy(tmp_path, [{"id": "VG005", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "fail"
    assert report.findings[0].id == "VG005:required-workflows"
    assert ".github/workflows/verify.yml" in report.findings[0].message


def test_vg005_required_workflows_override(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "ci.yaml").write_text("name: ci\n", encoding="utf-8")
    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG005",
                "enabled": True,
                "config": {"required_workflows": ["ci.yaml"]},
            }
        ],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"
