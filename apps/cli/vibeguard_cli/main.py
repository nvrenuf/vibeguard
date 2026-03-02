from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from packages.core.policy_loader import PolicyLoadError, load_policy_bundle
from packages.gates.runner import run_gates
from packages.reporting.audit_pack import create_audit_pack

DEFAULT_POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")
DEFAULT_AUDIT_OUT_DIR = Path("out/audit-pack")
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def _sort_findings(report_json: dict[str, object]) -> None:
    findings = report_json.get("findings", [])
    if not isinstance(findings, list):
        return
    findings.sort(
        key=lambda item: (
            SEVERITY_ORDER.get(str(item.get("severity")), -1),
            str(item.get("gate_id", "")),
            str(item.get("path", "")),
            str(item.get("line", "")),
            str(item.get("id", "")),
        ),
    )


def _parse_format(output_format: str) -> str:
    if output_format == "json":
        return "json"
    if output_format == "sarif":
        raise ValueError(
            "--format sarif is reserved for Issue #8 and not available yet. "
            "Use --format json for now."
        )
    raise ValueError(f"Unsupported format: {output_format}")


def _should_fail(findings: list[dict[str, object]], fail_on: str) -> bool:
    threshold = SEVERITY_ORDER[fail_on]
    for finding in findings:
        severity = str(finding.get("severity", ""))
        if SEVERITY_ORDER.get(severity, -1) >= threshold:
            return True
    return False


def _validate_repo(repo: Path) -> None:
    if not repo.exists() or not repo.is_dir():
        raise ValueError("repo must be an existing directory")


def run_check(
    repo: Path,
    policy: Path,
    out: Path | None = None,
    *,
    fail_on: str = "high",
    output_format: str = "json",
) -> int:
    _validate_repo(repo)
    if fail_on not in SEVERITY_ORDER:
        raise ValueError("--fail-on must be one of: low, medium, high, critical")
    _parse_format(output_format)
    policy_bundle = load_policy_bundle(policy)
    report = run_gates(policy=policy_bundle, repo_path=repo)
    payload_obj = json.loads(report.to_json())
    _sort_findings(payload_obj)
    payload = json.dumps(payload_obj, indent=2, sort_keys=True)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
    else:
        print(payload)

    findings = payload_obj.get("findings", [])
    if not isinstance(findings, list):
        return 1
    return 1 if _should_fail(findings, fail_on) else 0


def run_audit_pack(
    repo: Path,
    policy: Path,
    out_dir: Path = DEFAULT_AUDIT_OUT_DIR,
    *,
    force_pack: bool = False,
) -> int:
    _validate_repo(repo)
    policy_bundle = load_policy_bundle(policy)
    report = run_gates(policy=policy_bundle, repo_path=repo)
    run_dir = create_audit_pack(
        repo_path=repo,
        policy_path=policy,
        findings_report=report,
        out_dir=out_dir,
    )
    print(str(run_dir))
    if force_pack:
        return 0
    return 0 if report.summary.overall_status == "pass" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibeguard", description="VibeGuard CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    check_cmd = sub.add_parser("check", help="Run checks")
    check_cmd.add_argument("repo", type=Path)
    check_cmd.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    check_cmd.add_argument("--out", type=Path, default=None)
    check_cmd.add_argument(
        "--fail-on",
        choices=["low", "medium", "high", "critical"],
        default="high",
        help="Exit non-zero when findings are at or above this severity threshold.",
    )
    check_cmd.add_argument(
        "--format",
        choices=["json", "sarif"],
        default="json",
        help=argparse.SUPPRESS,
    )

    audit_cmd = sub.add_parser("audit-pack", help="Create audit pack")
    audit_cmd.add_argument("repo", type=Path)
    audit_cmd.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    audit_cmd.add_argument("--out-dir", type=Path, default=DEFAULT_AUDIT_OUT_DIR)
    audit_cmd.add_argument(
        "--force-pack",
        action="store_true",
        help="Always exit 0 after writing the audit pack, even if findings fail.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            return run_check(
                repo=args.repo,
                policy=args.policy,
                out=args.out,
                fail_on=args.fail_on,
                output_format=args.format,
            )
        if args.command == "audit-pack":
            return run_audit_pack(
                repo=args.repo,
                policy=args.policy,
                out_dir=args.out_dir,
                force_pack=args.force_pack,
            )
    except (PolicyLoadError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
