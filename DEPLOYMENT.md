# Deployment Guide

## v0
VibeGuard is a local-first CLI. “Deployment” is:
- publishing a versioned package (future)
- running in CI via GitHub Actions

## CI usage (baseline)
- Install dependencies
- Run `make verify`
- (Phase 3) Run `vibeguard check` with a pinned policy bundle

See `.github/workflows/verify.yml`.
