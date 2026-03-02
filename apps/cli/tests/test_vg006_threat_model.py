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


def test_vg006_passes_when_required_sections_exist(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    content = (
        "# Threat Model\n\n"
        "## Assets\n"
        "## Actors\n"
        "## Trust boundaries\n"
        "## Key threats and mitigations\n"
    )
    (repo / "THREAT_MODEL.md").write_text(
        content,
        encoding="utf-8",
    )
    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG006",
                "enabled": True,
                "config": {},
            }
        ],
    )

    report = run_gates(load_policy_bundle(policy), repo)
    assert report.summary.overall_status == "pass"


def test_vg006_fails_when_missing_sections(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "THREAT_MODEL.md").write_text("# Threat Model\n\n## Assets\n", encoding="utf-8")
    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG006",
                "enabled": True,
                "config": {},
            }
        ],
    )

    report = run_gates(load_policy_bundle(policy), repo)
    assert report.summary.overall_status == "fail"
    assert report.findings[0].id == "VG006:missing-sections"
