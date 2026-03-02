import json
from pathlib import Path

import pytest
from packages.core.policy_loader import load_policy_bundle
from packages.core.wizard_compile import WizardCompileError, compile_wizard_to_policy

from vibeguard_cli.main import main

TEMPLATE_PATH = Path("wizard/template.yaml")


def test_compile_template_to_valid_policy(tmp_path: Path) -> None:
    out = tmp_path / "policy.yaml"
    exit_code = main(
        ["wizard", "compile", "--in", str(TEMPLATE_PATH), "--out", str(out)],
    )
    assert exit_code == 0
    assert out.is_file()

    bundle = load_policy_bundle(out)
    gate_ids = [gate.id for gate in bundle.gates]
    assert gate_ids == ["VG001", "VG002", "VG003", "VG004", "VG005"]


def test_compile_is_deterministic(tmp_path: Path) -> None:
    out = tmp_path / "policy.yaml"
    compile_wizard_to_policy(TEMPLATE_PATH, out)
    first = out.read_text(encoding="utf-8")
    compile_wizard_to_policy(TEMPLATE_PATH, out)
    second = out.read_text(encoding="utf-8")
    assert first == second

    parsed = json.loads(first)
    assert parsed["id"] == "wizard-generated"


def test_compile_fails_closed_on_invalid_schema(tmp_path: Path) -> None:
    invalid = tmp_path / "wizard.yaml"
    invalid.write_text("policy_id: x\npolicy_version: 0.1.0\ndescription: x\n", encoding="utf-8")
    out = tmp_path / "policy.yaml"

    with pytest.raises(WizardCompileError):
        compile_wizard_to_policy(invalid, out)
