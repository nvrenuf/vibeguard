# VibeGuard Backlog Order

**Milestone:** `v0.1`

1. #2 Freeze v0.1 scope and definitions
   - Lock scope boundaries and shared definitions for v0.1 delivery.
2. #3 Single canonical “VibeGuard Core” flow doc
   - Publish one canonical end-to-end Core flow for implementers.
3. #4 ✅ Implement policy bundle loader (PR #24)
   - Add deterministic policy bundle loading behavior.
4. #5 ✅ Implement policy schema validation (PR #24)
   - Validate policy bundles against the canonical schema.
5. #6 ✅ Add policy bundle versioning + metadata (PR #24)
   - Require version/provenance metadata in policy bundles.
6. #7 ✅ Define canonical Findings JSON format (PR #24)
   - Standardize Findings JSON schema for all outputs.
7. #8 Add SARIF output option
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
15. #16 CLI: implement vibeguard audit-pack fully
   - Complete vibeguard audit-pack command behavior and UX.
16. #17 CLI: add vibeguard init
   - Add init command for project bootstrap.
17. #18 ✅ CI: run vibeguard on PRs (PR #31)
   - Run VibeGuard checks in PR CI workflows.
18. #19 ✅ Add release versioning (PR #31)
   - Define automated release/versioning mechanics.
19. #20 Wizard spec-to-policy compiler
   - Compile wizard specs into policy bundles.
20. #21 Wizard template + docs
   - Ship wizard templates and authoring docs.
21. #22 Add threat model checks for agentic risk
   - Add hardening checks for agentic threat-model risk.
22. #23 Logging + redaction policy
   - Define and enforce logging/redaction policy.
