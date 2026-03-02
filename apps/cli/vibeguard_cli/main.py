from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Optional

import typer

app = typer.Typer(no_args_is_help=True)

DEFAULT_POLICY_PATH = Path("policies/bundles/baseline/policy.yaml")
DEFAULT_AUDIT_OUT_DIR = Path("out/audit-pack")


@app.command()
def check(
    repo: Annotated[Path, typer.Argument(help="Path to the repo to check")],
    policy: Annotated[
        Path,
        typer.Option(
            "--policy",
            help="Path to the policy bundle YAML",
        ),
    ] = DEFAULT_POLICY_PATH,
    out: Annotated[
        Optional[Path],  # noqa: UP007 - Typer parser in this stack rejects `Path | None`
        typer.Option(
            "--out",
            help="Write findings JSON to this path (defaults to stdout)",
        ),
    ] = None,
) -> None:
    """
    Run VibeGuard checks against a repository path using a policy bundle.
    """
    if not repo.exists() or not repo.is_dir():
        raise typer.BadParameter("repo must be an existing directory")

    if not policy.exists() or not policy.is_file():
        raise typer.BadParameter("policy must be an existing file")

    findings = {
        "overall_status": "pass",
        "repo": str(repo),
        "policy": str(policy),
        "findings": [],
    }

    payload = json.dumps(findings, indent=2)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
    else:
        typer.echo(payload)


@app.command()
def audit_pack(
    repo: Annotated[Path, typer.Argument(help="Path to the repo to package")],
    policy: Annotated[
        Path,
        typer.Option(
            "--policy",
            help="Path to the policy bundle YAML",
        ),
    ] = DEFAULT_POLICY_PATH,
    out_dir: Annotated[
        Path,
        typer.Option(
            "--out-dir",
            help="Output directory for the audit pack",
        ),
    ] = DEFAULT_AUDIT_OUT_DIR,
) -> None:
    """
    Create an audit-pack folder with stub artifacts (to be replaced by real outputs).
    """
    if not repo.exists() or not repo.is_dir():
        raise typer.BadParameter("repo must be an existing directory")

    if not policy.exists() or not policy.is_file():
        raise typer.BadParameter("policy must be an existing file")

    (out_dir / "reports").mkdir(parents=True, exist_ok=True)
    (out_dir / "evidence").mkdir(parents=True, exist_ok=True)

    (out_dir / "reports" / "findings.json").write_text(
        json.dumps({"overall_status": "pass"}, indent=2),
        encoding="utf-8",
    )

    (out_dir / "reports" / "summary.md").write_text(
        "# VibeGuard Audit Pack\n\nStub.\n",
        encoding="utf-8",
    )

    typer.echo(str(out_dir))


if __name__ == "__main__":
    app()
