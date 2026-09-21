# DollarResume

Build a resume in minutes: fill out a form (or import an existing PDF/DOCX resume and let AI
pre-fill it for you), watch a formatted resume take shape live, and get AI feedback with
one-click, user-approved edits before you export.

DollarResume is open source and free to self-host. A hosted version at `<your-domain-here>`
charges $1 per generate/save/update to cover AI and infrastructure costs — that billing layer
is optional and off by default in this repo (see [Self-hosting](#self-hosting) below).

## Features

- **Interactive resume builder** — live preview as you type, print-ready PDF export
- **Import an existing resume** — upload a PDF/DOCX/TXT resume; the backend extracts the text
  and an LLM structures it into the form for you to review and edit
- **AI resume checker** — a recruiter-style review (score, strengths, things to fix) plus
  concrete suggested edits (rewritten summary, stronger bullets, missing skills) that you
  approve individually before anything is applied
- **Optional billing** — gate generate/save/update behind a $1 Stripe charge, for anyone running
  a public hosted instance; fully disabled for local/self-hosted use by default

## Architecture

```
frontend/   static HTML/JS resume builder (no build step required)
backend/    FastAPI app — auth, database, AI endpoints, Stripe integration
```

The frontend talks to the backend only through its HTTP API, so either half can be swapped or
redeployed independently.

## Self-hosting

1. Clone the repo and copy `.env.example` to `.env`
2. Fill in `ANTHROPIC_API_KEY` (required) and a `DATABASE_URL` (Postgres)
3. Leave `BILLING_ENABLED=false` for a free, unrestricted local instance — Stripe keys aren't
   required in this mode
4. `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
5. Open `frontend/index.html` (or serve it via the backend — see `backend/app/main.py`)

To enable billing on your own hosted instance, set `BILLING_ENABLED=true` and provide
`STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET`.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for branch conventions
(`Development` → `Testing` → `main`) and how to get a PR reviewed.

## Security

Found a vulnerability? Please don't open a public issue — see [SECURITY.md](SECURITY.md) for
how to report it privately.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
