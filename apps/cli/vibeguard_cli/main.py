from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from packages.core.policy_loader import PolicyLoadError, load_policy_bundle
from packages.core.wizard_compile import WizardCompileError, compile_wizard_to_policy
from packages.gates.runner import run_gates
from packages.reporting.audit_pack import create_audit_pack

DEFAULT_POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")
DEFAULT_AUDIT_OUT_DIR = Path("out/audit-pack")
INIT_POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")
INIT_FOLDERS = [Path("out/audit-pack"), Path("out/findings"), Path("evidence")]
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
SARIF_LEVEL = {"low": "note", "medium": "warning", "high": "error", "critical": "error"}


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
    if output_format in {"json", "sarif"}:
        return output_format
    raise ValueError("--format must be one of: json, sarif")


def _to_sarif(report_json: dict[str, object]) -> dict[str, object]:
    findings = report_json.get("findings", [])
    if not isinstance(findings, list):
        findings = []

    rules_by_id: dict[str, dict[str, object]] = {}
    results: list[dict[str, object]] = []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        rule_id = str(finding.get("gate_id", "UNKNOWN"))
        rules_by_id.setdefault(
            rule_id,
            {
                "id": rule_id,
                "name": str(finding.get("title", rule_id)),
                "shortDescription": {"text": str(finding.get("title", rule_id))},
            },
        )
        result: dict[str, object] = {
            "ruleId": rule_id,
            "level": SARIF_LEVEL.get(str(finding.get("severity", "low")), "warning"),
            "message": {"text": str(finding.get("message", ""))},
        }
        path = finding.get("path")
        if isinstance(path, str) and path:
            location: dict[str, object] = {
                "physicalLocation": {
                    "artifactLocation": {"uri": path},
                },
            }
            line = finding.get("line")
            if isinstance(line, int) and line > 0:
                location["physicalLocation"]["region"] = {"startLine": line}  # type: ignore[index]
            result["locations"] = [location]
        results.append(result)

    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "vibeguard",
                        "rules": [rules_by_id[key] for key in sorted(rules_by_id)],
                    }
                },
                "results": results,
            }
        ],
    }


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
    if output_format == "sarif":
        payload_obj_out = _to_sarif(payload_obj)
        payload = json.dumps(payload_obj_out, indent=2, sort_keys=True)
    else:
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


def run_init(target_dir: Path, *, force: bool = False) -> int:
    target_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    src_policy = DEFAULT_POLICY_PATH
    dst_policy = target_dir / INIT_POLICY_PATH
    dst_policy.parent.mkdir(parents=True, exist_ok=True)

    if dst_policy.exists() and not force:
        raise ValueError(f"Refusing to overwrite existing file without --force: {dst_policy}")
    dst_policy.write_text(src_policy.read_text(encoding="utf-8"), encoding="utf-8")
    created.append(dst_policy)

    for rel in INIT_FOLDERS:
        folder = target_dir / rel
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            created.append(folder)

    print("Initialized VibeGuard project:")
    for item in created:
        print(f"- {item}")
    return 0


def run_wizard_compile(in_path: Path, out_path: Path) -> int:
    compiled = compile_wizard_to_policy(in_path=in_path, out_path=out_path)
    print(str(compiled))
    return 0


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

    init_cmd = sub.add_parser("init", help="Initialize VibeGuard files in a target directory")
    init_cmd.add_argument("target", nargs="?", type=Path, default=Path("."))
    init_cmd.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist.",
    )

    wizard_cmd = sub.add_parser("wizard", help="Wizard tooling")
    wizard_sub = wizard_cmd.add_subparsers(dest="wizard_command", required=True)
    wizard_compile = wizard_sub.add_parser("compile", help="Compile wizard YAML to policy YAML")
    wizard_compile.add_argument("--in", dest="in_path", type=Path, required=True)
    wizard_compile.add_argument("--out", dest="out_path", type=Path, required=True)
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
        if args.command == "init":
            return run_init(target_dir=args.target, force=args.force)
        if args.command == "wizard" and args.wizard_command == "compile":
            return run_wizard_compile(in_path=args.in_path, out_path=args.out_path)
    except (PolicyLoadError, WizardCompileError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
