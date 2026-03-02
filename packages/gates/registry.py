from __future__ import annotations

from packages.reporting.findings import Finding

from .base import Gate
from .types import GateContext

REQUIRED_FILES = [
    "README.md",
    "SECURITY.md",
    "ARCHITECTURE.md",
    "AGENTS.md",
    "ISSUE_ORDER.md",
]


class VG001RequiredFilesGate(Gate):
    id = "VG001"
    description = "Required repository files must exist at repo root"

    def run(self, ctx: GateContext) -> list[Finding]:
        missing = [name for name in REQUIRED_FILES if not (ctx.repo_path / name).is_file()]
        findings: list[Finding] = []
        for path in missing:
            findings.append(
                Finding(
                    id=f"VG001:{path}",
                    gate_id=self.id,
                    severity="high",
                    title=f"Missing required file: {path}",
                    message=(
                        f"Create {path} at repository root to satisfy VG001 required files policy."
                    ),
                    path=path,
                ),
            )
        return findings


GATE_REGISTRY: dict[str, type[Gate]] = {
    VG001RequiredFilesGate.id: VG001RequiredFilesGate,
}


def get_gate(gate_id: str) -> Gate | None:
    gate_cls = GATE_REGISTRY.get(gate_id)
    return gate_cls() if gate_cls else None
