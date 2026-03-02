# VibeGuard Backlog Order

**Milestone:** `v0.1`

1. #2 ✅ Freeze v0.1 scope and definitions (PR #37)
   - Lock scope boundaries and shared definitions for v0.1 delivery.
2. #3 ✅ Single canonical “VibeGuard Core” flow doc (PR #37)
   - Publish one canonical end-to-end Core flow for implementers.
3. #4 ✅ Implement policy bundle loader (PR #24)
   - Add deterministic policy bundle loading behavior.
4. #5 ✅ Implement policy schema validation (PR #24)
   - Validate policy bundles against the canonical schema.
5. #6 ✅ Add policy bundle versioning + metadata (PR #24)
   - Require version/provenance metadata in policy bundles.
6. #7 ✅ Define canonical Findings JSON format (PR #24)
   - Standardize Findings JSON schema for all outputs.
7. #8 ✅ Add SARIF output option (PR #36)
   - Provide SARIF as an alternate findings export.
8. #9 ✅ Implement gate runner framework (PR #25)
   - Create gate execution and aggregation framework.
9. #10 ✅ Implement baseline gates (VG001-VG005) (PR #25, #26, #27)
   - Implement baseline gate set VG001-VG005.
10. #11 ✅ Implement scope filters for gates (PR #26)
   - Support include/exclude scope filters for gate runs.
11. #12 ✅ Implement audit pack directory structure (PR #28)
   - Define canonical audit-pack directory layout.
12. #13 ✅ Manifest + hashing (PR #28)
   - Add manifest generation and file hashing.
13. #14 ✅ Environment + toolchain metadata capture (PR #28)
   - Capture environment/toolchain metadata in audit packs.
14. #15 ✅ CLI: implement vibeguard check fully (PR #33)
   - Complete vibeguard check command behavior and UX.
15. #16 ✅ CLI: implement vibeguard audit-pack fully (PR #34)
   - Complete vibeguard audit-pack command behavior and UX.
16. #17 ✅ CLI: add vibeguard init (PR #35)
   - Add init command for project bootstrap.
17. #18 ✅ CI: run vibeguard on PRs (PR #31)
   - Run VibeGuard checks in PR CI workflows.
18. #19 ✅ Add release versioning (PR #31)
   - Define automated release/versioning mechanics.
19. #20 ✅ Wizard spec-to-policy compiler (PR #38)
   - Compile wizard specs into policy bundles.
20. #21 ✅ Wizard template + docs (PR #38)
   - Ship wizard templates and authoring docs.
21. #22 ✅ Add threat model checks for agentic risk (PR #39)
   - Add hardening checks for agentic threat-model risk.
22. #23 ✅ Logging + redaction policy (PR #39)
   - Define and enforce logging/redaction policy.

## v0.2 backlog

**Milestone:** `v0.2`

1. #41 v0.2: SOC2 baseline policy bundle + strict bundle
   - Productize policy packs with baseline and strict compliance-oriented defaults.
2. #42 v0.2: Audit pack verify/sign
   - Add integrity verification/signing workflow for audit-pack outputs.
3. #43 v0.2: Policy bundle discovery + selection
   - Improve multi-bundle discovery and deterministic policy selection UX.
4. #44 v0.2: Secret scan improvements (entropy + allowlist UX)
   - Improve VG003 signal quality with entropy checks and better suppression ergonomics.
5. #45 v0.2: License/dependency gate improvements
   - Expand dependency/license checks with stronger SPDX-aware behavior.
6. #46 v0.2: Scan caching / incremental mode
   - Reduce scan runtime by skipping unchanged files safely.
7. #47 v0.2: CLI summary UX improvements
   - Add clearer human-readable CLI summary output without breaking machine formats.
8. #48 v0.2: vibeguard.yaml config support
   - Support repo-level defaults via an optional `vibeguard.yaml` config file.
9. #49 ✅ v0.2: Publish a reusable GitHub Action (PR #TBD)
   - Package VibeGuard as a reusable action for adoption in external repos.
