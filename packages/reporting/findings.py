from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal


@dataclass(slots=True)
class RunMetadata:
    repo: str
    policy_id: str
    policy_version: str
    generated_at: str | None = None


@dataclass(slots=True)
class Finding:
    id: str
    gate_id: str
    severity: Literal["low", "medium", "high", "critical"]
    title: str
    message: str
    path: str | None = None
    line: int | None = None


@dataclass(slots=True)
class Summary:
    overall_status: Literal["pass", "fail"]
    total_findings: int


@dataclass(slots=True)
class FindingsReport:
    run: RunMetadata
    summary: Summary
    findings: list[Finding] = field(default_factory=list)
    schema_version: str = "1.0"

    @classmethod
    def create(
        cls,
        *,
        repo: str,
        policy_id: str,
        policy_version: str,
        findings: list[Finding] | None = None,
        generated_at: str | None = None,
    ) -> FindingsReport:
        normalized_findings = findings or []
        timestamp = generated_at or datetime.now(timezone.utc).isoformat()  # noqa: UP017
        overall_status: Literal["pass", "fail"] = "pass" if not normalized_findings else "fail"
        return cls(
            run=RunMetadata(
                repo=repo,
                policy_id=policy_id,
                policy_version=policy_version,
                generated_at=timestamp,
            ),
            summary=Summary(overall_status=overall_status, total_findings=len(normalized_findings)),
            findings=normalized_findings,
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)
