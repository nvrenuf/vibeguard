import json
from pathlib import Path

from vibeguard_cli.main import run_check


def test_check_outputs_findings_json(tmp_path: Path, capsys) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    exit_code = run_check(repo, Path("policies/bundles/baseline/policy.yaml"))

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "1.0"
    assert payload["run"]["policy_id"] == "baseline"
    assert payload["summary"]["overall_status"] == "pass"
    assert payload["findings"] == []
