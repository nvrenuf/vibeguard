#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   REPO="<owner>/<repo>" bash tools/create_v01_backlog.sh
# Example:
#   REPO="nvrenuf/vibeguard" bash tools/create_v01_backlog.sh

: "${REPO:?Set REPO=owner/name before running}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required but not installed." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required but not installed." >&2
  exit 1
fi

labels=(
  "v0.1"
  "milestone:A-spec"
  "milestone:B-policy"
  "milestone:C-findings"
  "milestone:D-gates"
  "milestone:E-audit-pack"
  "milestone:F-cli"
  "milestone:G-ci"
  "milestone:H-wizard"
  "hardening"
)

for label in "${labels[@]}"; do
  if ! gh label list --repo "$REPO" --limit 200 --json name | jq -e --arg n "$label" '.[] | select(.name==$n)' >/dev/null; then
    gh label create "$label" --repo "$REPO" --color "1D76DB" --description "VibeGuard v0.1 tracking label"
  fi
done

if ! gh api "repos/$REPO/milestones" --paginate | jq -e '.[] | select(.title=="v0.1")' >/dev/null; then
  gh api -X POST "repos/$REPO/milestones" -f title='v0.1' -f description='VibeGuard v0.1 backlog'
fi

milestone_number=$(gh api "repos/$REPO/milestones" --paginate | jq -r '.[] | select(.title=="v0.1") | .number' | head -n1)

create_issue() {
  local title="$1"
  local labels_csv="$2"
  local intent="$3"
  local scope="$4"
  local acceptance="$5"
  local touchpoints="$6"
  local tests="$7"

  local body
  body=$(cat <<EOT
## Goal
$intent

## Scope
$scope

## Acceptance Criteria
$acceptance

## File touchpoints
$touchpoints

## Test expectations
$tests
EOT
)

  gh issue create \
    --repo "$REPO" \
    --title "$title" \
    --milestone "$milestone_number" \
    --label "$labels_csv" \
    --body "$body"
}

mapfile -t issue_urls < <(
create_issue "Freeze v0.1 scope and definitions" "v0.1,milestone:A-spec" \
"Lock the exact v0.1 in-scope/out-of-scope boundaries and key definitions used across specs and implementation." \
"Define terms, delivery boundaries, and non-goals for v0.1." \
"- Explicit in-scope and out-of-scope lists\n- Definition section for all core terms\n- Sign-off criteria for scope freeze" \
"- README.md\n- ARCHITECTURE.md\n- SPECS/" \
"- Add/refresh tests only when scope docs imply behavior changes\n- Validation via doc review checklist"
create_issue "Single canonical “VibeGuard Core” flow doc" "v0.1,milestone:A-spec" \
"Create one canonical end-to-end flow document that all contributors implement against." \
"Describe the full Core flow from policy load to findings and audit outputs." \
"- One canonical flow document merged\n- No conflicting parallel flow docs remain\n- Links from README/architecture are updated" \
"- ARCHITECTURE.md\n- docs/\n- SPECS/" \
"- Doc consistency checks\n- Terminology cross-check against #001"
create_issue "Implement policy bundle loader" "v0.1,milestone:B-policy" \
"Load policy bundles from supported locations with deterministic resolution behavior." \
"Implement loader entrypoints and error behavior for missing/invalid bundles." \
"- Loader resolves local bundle path(s)\n- Clear errors for invalid/missing inputs\n- Loader API documented" \
"- tools/\n- docs/\n- SPECS/" \
"- Unit tests for success/failure load paths\n- Fixture-based loader tests"
create_issue "Implement policy schema validation" "v0.1,milestone:B-policy" \
"Validate policy bundles against the canonical schema before execution." \
"Introduce validation pipeline and failure reporting." \
"- Schema validation blocks invalid policy bundles\n- Validation errors are actionable\n- Validation integrated in loader/check flow" \
"- SPECS/\n- tools/\n- docs/" \
"- Unit tests for valid/invalid schema cases\n- Regression tests for known invalid examples"
create_issue "Add policy bundle versioning + metadata" "v0.1,milestone:B-policy" \
"Attach explicit versioning and metadata to policy bundles for traceability." \
"Define metadata fields and enforce compatibility checks." \
"- Version field required\n- Metadata includes provenance details\n- Compatibility behavior documented" \
"- SPECS/\n- docs/\n- CHANGELOG.md" \
"- Schema/validation tests for version+metadata\n- Compatibility matrix tests"
create_issue "Define canonical Findings JSON format" "v0.1,milestone:C-findings" \
"Publish the canonical machine-readable findings schema for all gate outputs." \
"Define fields, severity, rule IDs, and evidence structures." \
"- Findings schema versioned and documented\n- Example payloads included\n- All emitters aligned to schema contract" \
"- SPECS/\n- docs/\n- README.md" \
"- Schema validation tests\n- Golden-file tests for sample findings"
create_issue "Add SARIF output option" "v0.1,milestone:C-findings" \
"Support SARIF output in addition to canonical Findings JSON." \
"Map findings fields to SARIF while preserving rule/evidence fidelity." \
"- CLI/output layer supports SARIF flag\n- SARIF passes schema checks\n- Mapping limitations documented" \
"- tools/\n- docs/\n- SPECS/" \
"- Tests for JSON->SARIF transformation\n- SARIF conformance validation"
create_issue "Implement gate runner framework" "v0.1,milestone:D-gates" \
"Build the framework that discovers, schedules, and executes gates consistently." \
"Define runner interfaces, lifecycle hooks, and result aggregation." \
"- Runner supports multiple gate executions\n- Deterministic execution order documented\n- Aggregated findings output available" \
"- tools/\n- SPECS/\n- docs/" \
"- Unit tests for runner lifecycle\n- Integration tests with sample gates"
create_issue "Implement baseline gates (VG001-VG005)" "v0.1,milestone:D-gates" \
"Implement the first baseline gate set VG001 through VG005." \
"Deliver rule logic, findings, and documentation for each baseline gate." \
"- VG001-VG005 implemented\n- Rule docs include rationale and examples\n- Findings align with canonical schema" \
"- SPECS/\n- docs/\n- tools/" \
"- Per-gate unit tests\n- End-to-end baseline suite test"
create_issue "Implement scope filters for gates" "v0.1,milestone:D-gates" \
"Allow gate execution to be filtered by scope/target selection." \
"Define include/exclude behavior and precedence." \
"- Include/exclude filter model documented\n- Runner applies filters deterministically\n- Filter decisions observable in output" \
"- tools/\n- docs/\n- SPECS/" \
"- Filter matrix tests\n- Runner integration tests with mixed scopes"
create_issue "Implement audit pack directory structure" "v0.1,milestone:E-audit-pack" \
"Define and generate the canonical audit-pack directory layout." \
"Specify required files/subdirectories and generation rules." \
"- Directory structure spec finalized\n- Generator produces expected structure\n- Missing artifacts handled explicitly" \
"- docs/\n- SPECS/\n- tools/" \
"- Golden snapshot tests for structure\n- Validation tests for required artifacts"
create_issue "Manifest + hashing" "v0.1,milestone:E-audit-pack" \
"Produce manifest and integrity hashes for audit-pack contents." \
"Define hash algorithms and manifest schema." \
"- Manifest includes all required files\n- Hash values reproducible\n- Tamper detection behavior documented" \
"- SPECS/\n- tools/\n- docs/" \
"- Deterministic hash tests\n- Manifest verification tests"
create_issue "Environment + toolchain metadata capture" "v0.1,milestone:E-audit-pack" \
"Capture runtime environment and toolchain metadata in audit packs." \
"Define minimum metadata set and redaction boundaries." \
"- Metadata schema documented\n- Capture integrated into audit-pack generation\n- Sensitive values excluded/redacted" \
"- docs/\n- tools/\n- SECURITY.md" \
"- Tests for presence of required metadata\n- Redaction tests"
create_issue "CLI: implement vibeguard check fully" "v0.1,milestone:F-cli" \
"Complete the vibeguard check command UX and behavior." \
"Wire command inputs, outputs, exit codes, and errors to runner/findings systems." \
"- Command supports documented flags\n- Exit codes reflect pass/fail/error states\n- Help text and docs updated" \
"- tools/\n- README.md\n- docs/" \
"- CLI integration tests\n- Exit-code behavior tests"
create_issue "CLI: implement vibeguard audit-pack fully" "v0.1,milestone:F-cli" \
"Complete the vibeguard audit-pack command for producing audit artifacts." \
"Integrate manifest/hashing/metadata into command output." \
"- Command produces canonical audit-pack\n- Output location and naming documented\n- Errors are actionable" \
"- tools/\n- docs/\n- README.md" \
"- CLI integration tests for generated packs\n- Negative tests for bad inputs"
create_issue "CLI: add vibeguard init" "v0.1,milestone:F-cli" \
"Add vibeguard init command for project bootstrap/config generation." \
"Define generated defaults and safety checks for existing files." \
"- Init creates expected baseline config\n- Existing-file behavior documented\n- Init output references next steps" \
"- tools/\n- docs/\n- README.md" \
"- CLI tests for fresh and existing dirs\n- Snapshot tests for generated files"
create_issue "CI: run vibeguard on PRs" "v0.1,milestone:G-ci" \
"Run VibeGuard checks in CI for pull requests." \
"Define workflow triggers and reporting semantics." \
"- CI workflow executes on PR events\n- Findings surfaced in logs/artifacts\n- Failure gates documented" \
"- .github/workflows/\n- docs/\n- README.md" \
"- Workflow dry-run checks\n- CI validation in sample PR"
create_issue "Add release versioning" "v0.1,milestone:G-ci" \
"Define and automate release versioning for v0.1 lifecycle." \
"Set version source of truth and release tagging behavior." \
"- Versioning strategy documented\n- Release tagging process defined\n- Changelog policy linked" \
"- CHANGELOG.md\n- docs/\n- .github/workflows/" \
"- Tests/checks for version bump logic\n- Release workflow validation"
create_issue "Wizard spec-to-policy compiler" "v0.1,milestone:H-wizard" \
"Build compiler workflow that turns wizard specs into policy bundles." \
"Define input schema and emitted policy compatibility requirements." \
"- Compiler input/output specs documented\n- Generated policy validates against schema\n- Error reporting is actionable" \
"- SPECS/\n- tools/\n- docs/" \
"- Compiler unit tests\n- End-to-end spec->policy tests"
create_issue "Wizard template + docs" "v0.1,milestone:H-wizard" \
"Provide starter templates and documentation for wizard-driven policy authoring." \
"Cover common authoring paths and troubleshooting." \
"- Template set published\n- Docs include examples and pitfalls\n- Links from main docs are present" \
"- docs/\n- SPECS/\n- README.md" \
"- Docs validation/lint\n- Template rendering tests"
create_issue "Add threat model checks for agentic risk" "v0.1,hardening" \
"Add checks focused on agentic threat-model risks and misuse patterns." \
"Define checks and mapping back to threat model controls." \
"- Threat-model checks documented and implemented\n- Findings map to risk categories\n- Integration with runner confirmed" \
"- THREAT_MODEL.md\n- SPECS/\n- tools/" \
"- Rule tests for each threat check\n- Integration tests in gate suite"
create_issue "Logging + redaction policy" "v0.1,hardening" \
"Formalize logging and redaction policy across CLI, runner, and audit output." \
"Specify what is never logged and how redaction is tested." \
"- Logging policy approved and documented\n- Redaction rules implemented where needed\n- Security docs updated" \
"- SECURITY.md\n- docs/\n- tools/" \
"- Redaction unit tests\n- Log output regression tests"
)

# Build ISSUE_ORDER.md from created issue URLs (which include numbers)
{
  echo "# VibeGuard Backlog Order"
  echo
  echo "**Milestone:** \\`v0.1\\`"
  echo
  i=1
  titles=(
    "Freeze v0.1 scope and definitions"
    "Single canonical “VibeGuard Core” flow doc"
    "Implement policy bundle loader"
    "Implement policy schema validation"
    "Add policy bundle versioning + metadata"
    "Define canonical Findings JSON format"
    "Add SARIF output option"
    "Implement gate runner framework"
    "Implement baseline gates (VG001-VG005)"
    "Implement scope filters for gates"
    "Implement audit pack directory structure"
    "Manifest + hashing"
    "Environment + toolchain metadata capture"
    "CLI: implement vibeguard check fully"
    "CLI: implement vibeguard audit-pack fully"
    "CLI: add vibeguard init"
    "CI: run vibeguard on PRs"
    "Add release versioning"
    "Wizard spec-to-policy compiler"
    "Wizard template + docs"
    "Add threat model checks for agentic risk"
    "Logging + redaction policy"
  )
  intents=(
    "Lock scope boundaries and shared definitions for v0.1 delivery."
    "Publish one canonical end-to-end Core flow for implementers."
    "Add deterministic policy bundle loading behavior."
    "Validate policy bundles against the canonical schema."
    "Require version/provenance metadata in policy bundles."
    "Standardize Findings JSON schema for all outputs."
    "Provide SARIF as an alternate findings export."
    "Create gate execution and aggregation framework."
    "Implement baseline gate set VG001-VG005."
    "Support include/exclude scope filters for gate runs."
    "Define canonical audit-pack directory layout."
    "Add manifest generation and file hashing."
    "Capture environment/toolchain metadata in audit packs."
    "Complete vibeguard check command behavior and UX."
    "Complete vibeguard audit-pack command behavior and UX."
    "Add init command for project bootstrap."
    "Run VibeGuard checks in PR CI workflows."
    "Define automated release/versioning mechanics."
    "Compile wizard specs into policy bundles."
    "Ship wizard templates and authoring docs."
    "Add hardening checks for agentic threat-model risk."
    "Define and enforce logging/redaction policy."
  )
  for url in "${issue_urls[@]}"; do
    num="${url##*/}"
    idx=$((i-1))
    echo "$i. #$num ${titles[$idx]}"
    echo "   - ${intents[$idx]}"
    i=$((i+1))
  done
} > ISSUE_ORDER.md

echo "Created ${#issue_urls[@]} issues and updated ISSUE_ORDER.md"
