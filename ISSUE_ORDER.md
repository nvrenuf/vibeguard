# VibeGuard Backlog Order

**Milestone:** `v0.1`

> This file is the canonical ordered execution list for VibeGuard v0.1.
> It must mirror GitHub issues in both order and issue numbers.
>
> In this environment, `gh` was not available (`command not found`).
> Run the exact commands in `tools/create_v01_backlog.sh` from a machine with GitHub CLI installed and authenticated.
> The script creates labels, ensures the `v0.1` milestone, creates all issues in order, and rewrites this file with the real GitHub issue numbers.

## Planned order (titles fixed)

1. Freeze v0.1 scope and definitions
2. Single canonical “VibeGuard Core” flow doc
3. Implement policy bundle loader
4. Implement policy schema validation
5. Add policy bundle versioning + metadata
6. Define canonical Findings JSON format
7. Add SARIF output option
8. Implement gate runner framework
9. Implement baseline gates (VG001-VG005)
10. Implement scope filters for gates
11. Implement audit pack directory structure
12. Manifest + hashing
13. Environment + toolchain metadata capture
14. CLI: implement vibeguard check fully
15. CLI: implement vibeguard audit-pack fully
16. CLI: add vibeguard init
17. CI: run vibeguard on PRs
18. Add release versioning
19. Wizard spec-to-policy compiler
20. Wizard template + docs
21. Add threat model checks for agentic risk
22. Logging + redaction policy
