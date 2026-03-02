from __future__ import annotations

import argparse
import sys
from pathlib import Path

import typer
from packages.core.policy_loader import PolicyLoadError, load_policy_bundle
from packages.core.version import __version__
from packages.gates.runner import run_gates
from packages.reporting.audit_pack import create_audit_pack

DEFAULT_POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")
DEFAULT_AUDIT_OUT_DIR = Path("out/audit-pack")

app = typer.Typer(add_completion=False)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"vibeguard {__version__}")
        raise typer.Exit()


@app.callback()
def version_callback(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        expose_value=False,
        help="Show VibeGuard version and exit.",
    ),
) -> None:
    return None


def _validate_repo(repo: Path) -> None:
    if not repo.exists() or not repo.is_dir():
        raise ValueError("repo must be an existing directory")


def run_check(repo: Path, policy: Path, out: Path | None = None) -> int:
    _validate_repo(repo)
    policy_bundle = load_policy_bundle(policy)
    report = run_gates(policy=policy_bundle, repo_path=repo)
    payload = report.to_json()
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0 if report.summary.overall_status == "pass" else 1


def run_audit_pack(repo: Path, policy: Path, out_dir: Path = DEFAULT_AUDIT_OUT_DIR) -> int:
    _validate_repo(repo)
    policy_bundle = load_policy_bundle(policy)
    report = run_gates(policy=policy_bundle, repo_path=repo)
    run_dir = create_audit_pack(
        repo_path=repo,
        policy_path=policy,
        findings_report=report,
        out_dir=out_dir,
        vibeguard_version=__version__,
    )
    print(str(run_dir))
    return 0 if report.summary.overall_status == "pass" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibeguard", description="VibeGuard CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check_cmd = sub.add_parser("check", help="Run checks")
    check_cmd.add_argument("repo", type=Path)
    check_cmd.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    check_cmd.add_argument("--out", type=Path, default=None)

    audit_cmd = sub.add_parser("audit-pack", help="Create audit pack")
    audit_cmd.add_argument("repo", type=Path)
    audit_cmd.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH)
    audit_cmd.add_argument("--out-dir", type=Path, default=DEFAULT_AUDIT_OUT_DIR)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            return run_check(repo=args.repo, policy=args.policy, out=args.out)
        if args.command == "audit-pack":
            return run_audit_pack(repo=args.repo, policy=args.policy, out_dir=args.out_dir)
    except (PolicyLoadError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
