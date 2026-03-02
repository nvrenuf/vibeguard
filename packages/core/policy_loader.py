from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class GateConfig:
    id: str
    enabled: bool = True
    include_paths: list[str] | None = None
    exclude_paths: list[str] | None = None
    config: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PolicyBundle:
    id: str
    version: str
    description: str
    gates: list[GateConfig]
    include_paths: list[str] | None = None
    exclude_paths: list[str] | None = None


class PolicyLoadError(ValueError):
    """Raised when a policy bundle cannot be read or validated."""


def _require_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PolicyLoadError(
            f"policy schema validation failed: '{key}' must be a non-empty string",
        )
    return value


def _parse_gate(item: Any, idx: int) -> GateConfig:
    if not isinstance(item, dict):
        raise PolicyLoadError(
            (
                f"policy schema validation failed: gates[{idx}] must be an object "
                "with id/enabled/config"
            ),
        )
    gate_id = item.get("id")
    if not isinstance(gate_id, str) or not gate_id:
        raise PolicyLoadError(
            f"policy schema validation failed: gates[{idx}].id must be a non-empty string",
        )
    enabled = item.get("enabled", True)
    if not isinstance(enabled, bool):
        raise PolicyLoadError(
            f"policy schema validation failed: gates[{idx}].enabled must be a boolean",
        )
    include_paths = _optional_str_list(item, "include_paths", f"gates[{idx}].include_paths")
    exclude_paths = _optional_str_list(item, "exclude_paths", f"gates[{idx}].exclude_paths")
    config = item.get("config", {})
    if not isinstance(config, dict):
        raise PolicyLoadError(
            f"policy schema validation failed: gates[{idx}].config must be an object",
        )
    return GateConfig(
        id=gate_id,
        enabled=enabled,
        include_paths=include_paths,
        exclude_paths=exclude_paths,
        config=config,
    )


def _optional_str_list(
    data: dict[str, Any],
    key: str,
    label: str | None = None,
) -> list[str] | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise PolicyLoadError(
            "policy schema validation failed: "
            f"'{label or key}' must be a list of non-empty strings",
        )
    return value


def load_policy_bundle(path: Path) -> PolicyBundle:
    if not path.exists() or not path.is_file():
        raise PolicyLoadError(f"policy file does not exist: {path}")

    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PolicyLoadError(f"invalid YAML in policy file {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise PolicyLoadError(f"policy file must contain a top-level mapping: {path}")

    gates = data.get("gates")
    if not isinstance(gates, list) or not gates:
        raise PolicyLoadError("policy schema validation failed: 'gates' must be a non-empty list")

    return PolicyBundle(
        id=_require_str(data, "id"),
        version=_require_str(data, "version"),
        description=_require_str(data, "description"),
        include_paths=_optional_str_list(data, "include_paths"),
        exclude_paths=_optional_str_list(data, "exclude_paths"),
        gates=[_parse_gate(item, idx) for idx, item in enumerate(gates)],
    )
