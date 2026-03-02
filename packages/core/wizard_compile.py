from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .policy_loader import PolicyLoadError, load_policy_bundle


class WizardCompileError(ValueError):
    """Raised when wizard input cannot be compiled to a policy bundle."""


def _require_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WizardCompileError(
            f"wizard schema validation failed: '{key}' must be a non-empty string",
        )
    return value


def _require_str_list(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise WizardCompileError(
            f"wizard schema validation failed: '{key}' must be a non-empty list",
        )
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise WizardCompileError(
            f"wizard schema validation failed: '{key}' entries must be non-empty strings",
        )
    return value


def _optional_str_list(data: dict[str, Any], key: str) -> list[str] | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, list):
        raise WizardCompileError(f"wizard schema validation failed: '{key}' must be a list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise WizardCompileError(
            f"wizard schema validation failed: '{key}' entries must be non-empty strings",
        )
    return value


def _compile_gate_entries(gate_ids: list[str]) -> list[dict[str, Any]]:
    compiled: list[dict[str, Any]] = []
    for gate_id in gate_ids:
        compiled.append(
            {
                "id": gate_id,
                "enabled": True,
                "config": {},
            },
        )
    return compiled


def compile_wizard_to_policy(in_path: Path, out_path: Path) -> Path:
    if not in_path.exists() or not in_path.is_file():
        raise WizardCompileError(f"wizard input file does not exist: {in_path}")

    try:
        raw: Any = yaml.safe_load(in_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise WizardCompileError(f"invalid YAML in wizard file {in_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise WizardCompileError("wizard schema validation failed: top-level must be a mapping")

    gate_ids = _require_str_list(raw, "gate_ids")
    policy: dict[str, Any] = {
        "id": _require_str(raw, "policy_id"),
        "version": _require_str(raw, "policy_version"),
        "description": _require_str(raw, "description"),
        "include_paths": _optional_str_list(raw, "include_paths") or ["**"],
        "exclude_paths": _optional_str_list(raw, "exclude_paths") or [".git/**"],
        "gates": _compile_gate_entries(gate_ids),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(policy, indent=2, sort_keys=True), encoding="utf-8")

    try:
        load_policy_bundle(out_path)
    except PolicyLoadError as exc:
        raise WizardCompileError(f"compiled policy failed validation: {exc}") from exc

    return out_path
