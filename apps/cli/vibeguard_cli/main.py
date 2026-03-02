from __future__ import annotations

import json
from pathlib import Path

import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def check(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    policy: Path = typer.Option(
        Path("policies/bundles/baseline/policy.yaml"),
        "--policy",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    out: Path | None = typer.Option(None, "--out", help="Write findings JSON to this path"),
):
    """
    Run VibeGuard gates against a repository checkout.

    v0: outputs a stub findings report and validates policy file readability.
    """
    findings = {
        "overall_status": "pass",
        "repo": str(repo),
        "policy": str(policy),
        "gates": [],
        "findings": [],
    }

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    else:
        typer.echo(json.dumps(findings, indent=2))


@app.command()
def audit_pack(
    repo: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    policy: Path = typer.Option(
        Path("policies/bundles/baseline/policy.yaml"),
        "--policy",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    out_dir: Path = typer.Option(Path("out/audit-pack"), "--out-dir"),
):
    """
    Export an audit pack folder.

    v0: creates the folder structure and writes placeholder manifest/report.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "reports").mkdir(exist_ok=True)
    (out_dir / "policy_bundle").mkdir(exist_ok=True)

    # Placeholder artifacts (real implementation in Phase 2)
    (out_dir / "reports" / "findings.json").write_text(
        json.dumps({"overall_status": "pass"}, indent=2), encoding="utf-8"
    )
    (out_dir / "reports" / "summary.md").write_text(
        "# VibeGuard Audit Pack\n\nStub.\n", encoding="utf-8"
    )

    typer.echo(str(out_dir))


if __name__ == "__main__":
    app()
