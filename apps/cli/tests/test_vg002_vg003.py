import json
from dataclasses import asdict
from pathlib import Path

from packages.core.policy_loader import load_policy_bundle
from packages.gates.runner import run_gates


def _policy(tmp_path: Path, gates: list[dict], include_paths=None, exclude_paths=None) -> Path:
    payload = {
        "id": "test",
        "version": "0.1.0",
        "description": "test",
        "gates": gates,
    }
    if include_paths is not None:
        payload["include_paths"] = include_paths
    if exclude_paths is not None:
        payload["exclude_paths"] = exclude_paths
    path = tmp_path / "policy.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_vg002_passes_when_forbidden_absent(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    policy = _policy(tmp_path, [{"id": "VG002", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg002_fails_when_forbidden_exists(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "dist").mkdir()
    policy = _policy(tmp_path, [{"id": "VG002", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "fail"
    assert report.findings[0].id == "VG002:dist"


def test_vg002_allowed_path_is_ignored(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "dist").mkdir()
    policy = _policy(
        tmp_path,
        [{"id": "VG002", "enabled": True, "config": {"forbidden": ["dist"], "allow": ["dist"]}}],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg002_findings_are_deterministic(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "build").mkdir()
    (repo / "dist").mkdir()
    policy = _policy(
        tmp_path,
        [{"id": "VG002", "enabled": True, "config": {"forbidden": ["dist", "build"], "allow": []}}],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert [finding.id for finding in report.findings] == ["VG002:build", "VG002:dist"]


def test_vg003_detects_patterns_without_secret_value_leak(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "secrets.txt").write_text(
        "AKIA1234567890ABCDEF\n"
        "ghp_superSecretTokenValue\n"
        "xoxb-1234567890-abcdefghijkl\n"
        "-----BEGIN PRIVATE KEY-----\n",
        encoding="utf-8",
    )
    policy = _policy(tmp_path, [{"id": "VG003", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert len(report.findings) == 4
    serialized = json.dumps([asdict(finding) for finding in report.findings])
    assert "superSecretTokenValue" not in serialized


def test_vg003_allow_paths_excludes_files(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "ignore.txt").write_text("AKIA1234567890ABCDEF\n", encoding="utf-8")
    policy = _policy(
        tmp_path,
        [{"id": "VG003", "enabled": True, "config": {"allow_paths": ["ignore.txt"]}}],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg003_allow_patterns_suppresses_finding(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "file.txt").write_text("AKIA1234567890ABCDEF\n", encoding="utf-8")
    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG003",
                "enabled": True,
                "config": {"allow_patterns": [r"AKIA[0-9A-Z]{16}"]},
            }
        ],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg003_skips_binary_file(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "blob.bin").write_bytes(b"\x00AKIA1234567890ABCDEF")
    policy = _policy(tmp_path, [{"id": "VG003", "enabled": True, "config": {}}])

    report = run_gates(load_policy_bundle(policy), repo)

    assert report.summary.overall_status == "pass"


def test_vg003_uses_scope_filters_and_gate_override(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "safe.txt").write_text("AKIA1234567890ABCDEF\n", encoding="utf-8")
    (repo / "scan.txt").write_text("AKIA1234567890ABCDEF\n", encoding="utf-8")

    policy = _policy(
        tmp_path,
        [
            {
                "id": "VG003",
                "enabled": True,
                "include_paths": ["scan.txt"],
                "config": {},
            }
        ],
        include_paths=["safe.txt"],
    )

    report = run_gates(load_policy_bundle(policy), repo)

    assert len(report.findings) == 1
    assert report.findings[0].path == "scan.txt"
