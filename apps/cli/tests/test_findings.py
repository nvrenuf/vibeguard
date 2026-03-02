import json

from packages.reporting.findings import Finding, FindingsReport


def test_findings_report_deterministic_json() -> None:
    report = FindingsReport.create(
        repo=".",
        policy_id="baseline",
        policy_version="0.1.0",
        generated_at="2026-01-01T00:00:00+00:00",
        findings=[],
    )

    payload = report.to_json()
    loaded = json.loads(payload)

    assert loaded["schema_version"] == "1.0"
    assert loaded["run"]["generated_at"] == "2026-01-01T00:00:00+00:00"
    assert loaded["summary"] == {"overall_status": "pass", "total_findings": 0}
    assert loaded["findings"] == []


def test_findings_report_required_fields() -> None:
    finding = Finding(
        id="VG001",
        gate_id="repo.required_files",
        severity="high",
        title="Missing required file",
        message="REPO_CONTRACT.md is missing",
    )
    report = FindingsReport.create(
        repo=".",
        policy_id="baseline",
        policy_version="0.1.0",
        generated_at="2026-01-01T00:00:00+00:00",
        findings=[finding],
    )

    assert report.summary.overall_status == "fail"
    assert report.summary.total_findings == 1
    assert report.findings[0].id == "VG001"
