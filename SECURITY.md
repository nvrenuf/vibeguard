# Security Policy

## Reporting vulnerabilities
If you believe you have found a security issue, report it via your company’s security channel
(or a private email/security ticket system). Do not file public issues for vulnerabilities.

## Secure defaults
This repo enforces:
- secrets scanning in CI
- least privilege principles
- input validation requirements
- audit logging for security-relevant operations

## Secrets handling
- Never commit secrets to git.
- Use environment variables locally (`.env` files must be gitignored).
- Use your organization’s secret manager in production.

## Security review triggers
Additional review is required when changes involve:
- auth/authz
- cryptography
- secrets management
- user/session handling
- tenant isolation / multi-tenancy
- data ingestion pipelines
- tool/action execution (agentic behaviors)
