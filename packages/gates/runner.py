from __future__ import annotations

from pathlib import Path

from packages.core.policy_loader import PolicyBundle
from packages.reporting.findings import Finding, FindingsReport

from .registry import get_gate
from .types import GateContext


def run_gates(policy: PolicyBundle, repo_path: Path) -> FindingsReport:
    findings: list[Finding] = []

    for gate_config in policy.gates:
        if not gate_config.enabled:
            continue
        gate = get_gate(gate_config.id)
        if gate is None:
            findings.append(
                Finding(
                    id=f"UNKNOWN_GATE:{gate_config.id}",
                    gate_id=gate_config.id,
                    severity="high",
                    title=f"Unknown gate id: {gate_config.id}",
                    message=(
                        "Policy references a gate id that is not registered. "
                        "Failing closed by design."
                    ),
                ),
            )
            continue

        ctx = GateContext(repo_path=repo_path, policy=policy, gate_config=gate_config)
        findings.extend(gate.run(ctx))

    return FindingsReport.create(
        repo=str(repo_path),
        policy_id=policy.id,
        policy_version=policy.version,
        findings=findings,
    )
