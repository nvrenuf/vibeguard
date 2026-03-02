from __future__ import annotations

from abc import ABC, abstractmethod

from packages.reporting.findings import Finding

from .types import GateContext


class Gate(ABC):
    id: str
    description: str

    @abstractmethod
    def run(self, ctx: GateContext) -> list[Finding]:
        """Execute this gate against the given context."""
