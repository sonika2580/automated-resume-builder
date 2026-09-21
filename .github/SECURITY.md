# Security Policy

## Reporting a vulnerability

This project handles personal data (resumes, contact details) and payment flows, so please
report suspected vulnerabilities privately rather than opening a public issue.

- Email: **security@\<your-domain-here\>** (replace with a real address you monitor)
- Please include: a description of the issue, steps to reproduce, and the potential impact
- You should get an acknowledgment within a few days; we'll keep you updated as we investigate
  and fix

Please don't publicly disclose the issue until we've had a reasonable chance to address it.

## Areas that deserve extra scrutiny

Given what this app does, reports involving the following are especially welcome:

- Stripe webhook signature verification / replay / double-credit bugs
- Anything that could leak one user's saved resume or credit balance to another user
- Auth/session handling issues
- Injection in the AI-parsed import flow (untrusted file content flowing into prompts or storage)

## Supported versions

Only the `main` branch (production) receives security fixes. Please make sure you're on the
latest release before reporting.
