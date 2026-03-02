from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from packages.core.policy_loader import GateConfig, PolicyBundle
from packages.reporting.findings import Finding


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class GateContext:
    repo_path: Path
    policy: PolicyBundle
    gate_config: GateConfig


@dataclass(slots=True)
class GateResult:
    gate_id: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.findings
