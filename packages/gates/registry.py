from __future__ import annotations

import re
from fnmatch import fnmatch
from pathlib import Path

from packages.core.path_scope import iter_scoped_paths
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

DEFAULT_FORBIDDEN = [
    ".env",
    ".next",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "secrets",
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


class VG002ForbiddenDirectoriesGate(Gate):
    id = "VG002"
    description = "Forbidden repository root paths must not exist"

    def run(self, ctx: GateContext) -> list[Finding]:
        forbidden = sorted(ctx.gate_config.config.get("forbidden", DEFAULT_FORBIDDEN))
        allow = set(ctx.gate_config.config.get("allow", []))

        findings: list[Finding] = []
        for raw_path in forbidden:
            if raw_path in allow:
                continue
            path = Path(raw_path.rstrip("/"))
            if (ctx.repo_path / path).exists():
                findings.append(
                    Finding(
                        id=f"VG002:{path.as_posix()}",
                        gate_id=self.id,
                        severity="high",
                        title=f"Forbidden path present: {path.as_posix()}",
                        message=(
                            "Remove generated/build artifacts or secrets from repository root. "
                            "If this path is intentional, explicitly add it to VG002 config.allow."
                        ),
                        path=path.as_posix(),
                    ),
                )
        return findings


class VG003BasicSecretScanGate(Gate):
    id = "VG003"
    description = "Basic high-confidence secret pattern scan"

    _PATTERNS = [
        ("AWS Access Key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
        ("GitHub Token", re.compile(r"(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]+")),
        ("Slack Token", re.compile(r"xox(?:b|p|a)-[A-Za-z0-9-]+")),
        ("Private Key Block", re.compile(r"BEGIN PRIVATE KEY")),
    ]

    def run(self, ctx: GateContext) -> list[Finding]:
        include_paths = ctx.gate_config.include_paths or ctx.policy.include_paths
        exclude_paths = ctx.gate_config.exclude_paths or ctx.policy.exclude_paths
        allow_paths = ctx.gate_config.config.get("allow_paths", [])
        allow_patterns = [
            re.compile(pattern)
            for pattern in ctx.gate_config.config.get("allow_patterns", [])
        ]

        scoped_files = iter_scoped_paths(
            ctx.repo_path,
            include_paths=include_paths,
            exclude_paths=exclude_paths,
            files_only=True,
        )

        findings: list[Finding] = []
        for rel_path in scoped_files:
            rel_str = rel_path.as_posix()
            if any(fnmatch(rel_str, pattern) for pattern in allow_paths):
                continue

            raw = (ctx.repo_path / rel_path).read_bytes()
            if b"\x00" in raw:
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue

            for line_no, line in enumerate(text.splitlines(), start=1):
                for pattern_name, pattern in self._PATTERNS:
                    for match in pattern.finditer(line):
                        matched_text = match.group(0)
                        if any(allowed.search(matched_text) for allowed in allow_patterns):
                            continue
                        findings.append(
                            Finding(
                                id=f"VG003:{rel_str}:{line_no}:{pattern_name}",
                                gate_id=self.id,
                                severity="high",
                                title=f"Potential secret detected ({pattern_name})",
                                message=(
                                    "Potential credential material detected. Rotate/revoke exposed "
                                    "credentials, remove secrets from the repository, and store "
                                    "secrets in a secure secret manager."
                                ),
                                path=rel_str,
                                line=line_no,
                            ),
                        )
        return findings


GATE_REGISTRY: dict[str, type[Gate]] = {
    VG001RequiredFilesGate.id: VG001RequiredFilesGate,
    VG002ForbiddenDirectoriesGate.id: VG002ForbiddenDirectoriesGate,
    VG003BasicSecretScanGate.id: VG003BasicSecretScanGate,
}


def get_gate(gate_id: str) -> Gate | None:
    gate_cls = GATE_REGISTRY.get(gate_id)
    return gate_cls() if gate_cls else None
