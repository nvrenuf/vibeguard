# Deployment Guide

This template is deployment-agnostic. Fill in your actual deployment model.

## Supported modes (examples)
- Local Docker Compose
- Kubernetes
- AWS ECS/Fargate
- Bare metal

## Minimum requirements
- Secrets injected via environment or secret manager
- Immutable builds and reproducible deploys
- CI must produce build artifacts or images

## Deployment checklist (minimum)
- [ ] Configuration documented
- [ ] Secrets managed correctly
- [ ] Observability configured (logs/metrics)
- [ ] Rollback strategy defined
