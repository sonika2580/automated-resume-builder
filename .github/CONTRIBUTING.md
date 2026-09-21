# Contributing to DollarResume

Thanks for considering a contribution — this guide covers the basics of getting a change in.

## Branch model

- `main` — production. Only merged from `Testing` via a reviewed PR.
- `Testing` — release candidate. Merged from `Development` once a batch of work is stable.
- `Development` — active work lands here first.

If you're contributing a feature or fix, branch off `Development`:

```bash
git checkout Development
git pull
git checkout -b your-name/short-description
```

## Making a change

1. Open an issue first for anything non-trivial, so the approach can be discussed before you
   invest time in it. Small fixes (typos, obvious bugs) can skip straight to a PR.
2. Keep PRs focused — one logical change per PR is much easier to review than a bundle of
   unrelated fixes.
3. Write a clear PR description: what changed, why, and how you tested it.
4. Target the `Development` branch, not `main`.
5. Make sure existing tests pass and add tests for new behavior where it makes sense
   (especially around the credits/billing logic — that code path should never be undertested).

## Code style

- Backend: Python, formatted with `black`, linted with `ruff` (run both before pushing)
- Frontend: no build step; keep the single-file structure unless a change genuinely requires
  splitting it up — open an issue to discuss first if you think it does

## Reporting bugs

Open a GitHub issue using the bug report template. Include steps to reproduce, what you
expected, and what actually happened. For security vulnerabilities, see
[SECURITY.md](SECURITY.md) instead of a public issue.

## Code of conduct

Participation in this project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
