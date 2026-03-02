from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.core.version import __version__
from packages.reporting.findings import FindingsReport

SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)  # noqa: UP017


def _format_created_at(ts: datetime) -> str:
    return ts.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git_sha(repo_path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--short=7", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    sha = result.stdout.strip()
    return sha or None


def _build_run_id(created_at: datetime, git_sha: str | None) -> str:
    timestamp = created_at.strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{git_sha or 'nogit'}"


def _severity_counts(findings_report: FindingsReport) -> dict[str, int]:
    counts = {severity: 0 for severity in SEVERITY_ORDER}
    for finding in findings_report.findings:
        if finding.severity in counts:
            counts[finding.severity] += 1
    return counts


def _write_summary(
    summary_path: Path,
    run_id: str,
    findings_report: FindingsReport,
) -> None:
    severity_counts = _severity_counts(findings_report)
    lines = [
        "# VibeGuard Audit Pack Summary",
        "",
        f"- run_id: {run_id}",
        f"- overall_status: {findings_report.summary.overall_status}",
        f"- policy_id: {findings_report.run.policy_id}",
        f"- policy_version: {findings_report.run.policy_version}",
        "",
        "## Findings by severity",
        "",
    ]
    lines.extend(f"- {severity}: {severity_counts[severity]}" for severity in SEVERITY_ORDER)
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _collect_hashed_files(run_dir: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_path = path.relative_to(run_dir).as_posix()
        if rel_path == "manifest.json":
            continue
        files.append(
            {
                "path": rel_path,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            },
        )
    return files


def write_manifest(
    manifest_path: Path,
    *,
    vibeguard_version: str,
    created_at_utc: str,
    run_id: str,
    repo_path: Path,
    git_commit: str | None,
    policy_path: Path,
    overall_status: str,
    files: list[dict[str, Any]],
) -> None:
    manifest = {
        "vibeguard_version": vibeguard_version,
        "created_at_utc": created_at_utc,
        "run_id": run_id,
        "repo_path": str(repo_path),
        "git_commit": git_commit,
        "policy_path": str(policy_path),
        "overall_status": overall_status,
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "os": platform.platform(),
        "files": files,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def create_audit_pack(
    repo_path: Path,
    policy_path: Path,
    findings_report: FindingsReport,
    out_dir: Path,
    *,
    run_id: str | None = None,
    created_at: datetime | None = None,
    vibeguard_version: str = __version__,
) -> Path:
    created = created_at or _utc_now()
    git_sha = _git_sha(repo_path)
    resolved_run_id = run_id or _build_run_id(created, git_sha)
    run_dir = out_dir / resolved_run_id

    reports_dir = run_dir / "reports"
    evidence_dir = run_dir / "evidence"
    policy_bundle_dir = run_dir / "policy_bundle"
    reports_dir.mkdir(parents=True, exist_ok=False)
    evidence_dir.mkdir(parents=True, exist_ok=False)
    policy_bundle_dir.mkdir(parents=True, exist_ok=False)

    findings_path = reports_dir / "findings.json"
    summary_path = reports_dir / "summary.md"
    policy_snapshot_path = policy_bundle_dir / "policy.yaml"
    manifest_path = run_dir / "manifest.json"

    findings_path.write_text(findings_report.to_json() + "\n", encoding="utf-8")
    _write_summary(summary_path, resolved_run_id, findings_report)
    policy_snapshot_path.write_text(policy_path.read_text(encoding="utf-8"), encoding="utf-8")

    files = _collect_hashed_files(run_dir)
    write_manifest(
        manifest_path,
        vibeguard_version=vibeguard_version,
        created_at_utc=_format_created_at(created),
        run_id=resolved_run_id,
        repo_path=repo_path,
        git_commit=git_sha,
        policy_path=policy_path,
        overall_status=findings_report.summary.overall_status,
        files=files,
    )

    return run_dir
