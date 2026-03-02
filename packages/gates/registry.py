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

DEFAULT_LICENSE_PATHS = ["LICENSE", "LICENSE.md", "LICENSE.txt"]
DEFAULT_NOTICES_PATHS = ["THIRD_PARTY_NOTICES.md", "THIRD_PARTY_NOTICES.txt"]
DEFAULT_REQUIRED_WORKFLOWS = [".github/workflows/verify.yml"]
DEFAULT_THREAT_MODEL_PATH = "THREAT_MODEL.md"
DEFAULT_THREAT_MODEL_SECTIONS = [
    "Assets",
    "Actors",
    "Trust boundaries",
    "Key threats and mitigations",
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


class VG004LicenseAndNoticesGate(Gate):
    id = "VG004"
    description = "Repository license and third-party notices presence"

    def run(self, ctx: GateContext) -> list[Finding]:
        require_license = ctx.gate_config.config.get("require_license", True)
        require_notices = ctx.gate_config.config.get("require_third_party_notices", False)
        license_paths = ctx.gate_config.config.get("license_paths", DEFAULT_LICENSE_PATHS)
        notices_paths = ctx.gate_config.config.get("notices_paths", DEFAULT_NOTICES_PATHS)

        findings: list[Finding] = []

        if require_license and not any((ctx.repo_path / path).is_file() for path in license_paths):
            findings.append(
                Finding(
                    id="VG004:license",
                    gate_id=self.id,
                    severity="high",
                    title="Missing repository license file",
                    message=(
                        "Add a repository license file at one of the configured paths "
                        f"({', '.join(license_paths)})."
                    ),
                    path=license_paths[0],
                ),
            )

        if require_notices and not any((ctx.repo_path / path).is_file() for path in notices_paths):
            findings.append(
                Finding(
                    id="VG004:third-party-notices",
                    gate_id=self.id,
                    severity="high",
                    title="Missing third-party notices file",
                    message=(
                        "Add third-party notices at one of the configured paths "
                        f"({', '.join(notices_paths)})."
                    ),
                    path=notices_paths[0],
                ),
            )

        return findings


class VG005RequiredWorkflowsGate(Gate):
    id = "VG005"
    description = "Required CI workflow files must exist"

    def run(self, ctx: GateContext) -> list[Finding]:
        required_workflows = ctx.gate_config.config.get(
            "required_workflows",
            DEFAULT_REQUIRED_WORKFLOWS,
        )
        missing = [path for path in required_workflows if not (ctx.repo_path / path).is_file()]
        if not missing:
            return []

        return [
            Finding(
                id="VG005:required-workflows",
                gate_id=self.id,
                severity="high",
                title="Missing required CI workflow files",
                message=(
                    "Add the missing workflow files: "
                    f"{', '.join(missing)}."
                ),
                path=missing[0],
            ),
        ]


class VG006ThreatModelStructureGate(Gate):
    id = "VG006"
    description = "Threat model document must exist and contain required sections"

    def run(self, ctx: GateContext) -> list[Finding]:
        threat_model_path = ctx.gate_config.config.get(
            "threat_model_path",
            DEFAULT_THREAT_MODEL_PATH,
        )
        required_sections = ctx.gate_config.config.get(
            "required_sections",
            DEFAULT_THREAT_MODEL_SECTIONS,
        )

        path = ctx.repo_path / threat_model_path
        if not path.is_file():
            return [
                Finding(
                    id="VG006:missing-threat-model",
                    gate_id=self.id,
                    severity="high",
                    title="Missing threat model document",
                    message=f"Add {threat_model_path} with required threat model sections.",
                    path=threat_model_path,
                ),
            ]

        content = path.read_text(encoding="utf-8")
        heading_lines = [line.strip().lstrip("#").strip() for line in content.splitlines()]

        missing = [section for section in required_sections if section not in heading_lines]
        if not missing:
            return []

        return [
            Finding(
                id="VG006:missing-sections",
                gate_id=self.id,
                severity="high",
                title="Threat model missing required sections",
                message=f"Add these sections to {threat_model_path}: {', '.join(missing)}.",
                path=threat_model_path,
            ),
        ]


GATE_REGISTRY: dict[str, type[Gate]] = {
    VG001RequiredFilesGate.id: VG001RequiredFilesGate,
    VG002ForbiddenDirectoriesGate.id: VG002ForbiddenDirectoriesGate,
    VG003BasicSecretScanGate.id: VG003BasicSecretScanGate,
    VG004LicenseAndNoticesGate.id: VG004LicenseAndNoticesGate,
    VG005RequiredWorkflowsGate.id: VG005RequiredWorkflowsGate,
    VG006ThreatModelStructureGate.id: VG006ThreatModelStructureGate,
}


def get_gate(gate_id: str) -> Gate | None:
    gate_cls = GATE_REGISTRY.get(gate_id)
    return gate_cls() if gate_cls else None
