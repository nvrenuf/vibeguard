from pathlib import Path

import pytest
from packages.core.policy_loader import PolicyLoadError, load_policy_bundle


def test_load_policy_bundle_valid() -> None:
    policy = load_policy_bundle(Path("policies/bundles/baseline/policy.yaml"))
    assert policy.id == "baseline"
    assert policy.version == "0.1.0"
    assert len(policy.gates) >= 1


def test_load_policy_bundle_missing_file() -> None:
    with pytest.raises(PolicyLoadError, match="does not exist"):
        load_policy_bundle(Path("missing/policy.yaml"))


def test_load_policy_bundle_invalid_yaml(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text("id: [", encoding="utf-8")

    with pytest.raises(PolicyLoadError, match="invalid YAML"):
        load_policy_bundle(policy_path)


def test_load_policy_bundle_schema_violation(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(
        '{"id":"baseline","version":"0.1.0","description":"x","gates":[]}',
        encoding="utf-8",
    )

    with pytest.raises(PolicyLoadError, match="schema validation failed"):
        load_policy_bundle(policy_path)


def test_load_policy_bundle_scope_fields(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(
        '{"id":"baseline","version":"0.1.0","description":"x","include_paths":["src/**"],"exclude_paths":["tests/**"],"gates":[{"id":"VG001","enabled":true,"include_paths":["src/**"],"exclude_paths":["tmp/**"],"config":{}}]}',
        encoding="utf-8",
    )

    policy = load_policy_bundle(policy_path)

    assert policy.include_paths == ["src/**"]
    assert policy.exclude_paths == ["tests/**"]
    assert policy.gates[0].include_paths == ["src/**"]
    assert policy.gates[0].exclude_paths == ["tmp/**"]
