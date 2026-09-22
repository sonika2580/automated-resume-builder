# DollarResume — Project Task Breakdown

Stack: FastAPI (backend) · existing HTML/JS resume builder (frontend) · Postgres (Supabase) · Stripe · Anthropic API

Suggested flow: build features on `Development`, harden and QA on `Testing`, merge to `main` for release.
Each item below is sized to work as a single GitHub Issue — copy the `##` phase as a milestone and each
`- [ ]` line as an issue title.

---

## Milestone 0 — Repo & environment setup (`Development`)
- [ ] Add `/backend` (FastAPI) and `/frontend` (current HTML/JS app) folders to the repo
- [ ] Create `.env.example` listing required secrets (ANTHROPIC_API_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, DATABASE_URL, SUPABASE keys)
- [ ] Add `.gitignore` for `.env`, `__pycache__/`, `node_modules/`, build artifacts
- [ ] Set up branch protection on `main` (require PR + passing checks before merge)
- [ ] Add a basic `README.md`: what the project is, how to run it locally

## Milestone 1 — Backend foundation (`Development`)
- [ ] Scaffold FastAPI app with `/health` endpoint
- [ ] Add environment/config loading (pydantic Settings or python-dotenv)
- [ ] Add CORS config so the frontend origin can call the API
- [ ] Set up local dev workflow (uvicorn reload, requirements.txt or pyproject.toml)
- [ ] Add structured logging (so Stripe webhook and AI-call failures are traceable)

## Milestone 2 — Database & accounts (`Development`)
- [ ] Stand up Postgres (Supabase project, or self-hosted)
- [ ] Define schema: `users`, `resumes` (versioned), `credits_ledger`, `payments`
- [ ] Add auth (email/password or OAuth via Supabase Auth) — issue login/session tokens
- [ ] Add `/me` endpoint returning current user + credit balance
- [ ] Write migration scripts (Alembic) for the schema above

## Milestone 3 — AI features as real endpoints (`Development`)
- [ ] `POST /api/import` — accepts extracted resume text, calls Anthropic API server-side, returns structured JSON matching the frontend's resume schema
- [ ] `POST /api/check` — accepts resume JSON, returns score + strengths + improvements + suggested edits (same shape the frontend already expects)
- [ ] Move PDF/DOCX text extraction server-side (pdfplumber / python-docx) — simpler and more reliable than doing it in-browser
- [ ] Add request size limits + basic input validation on all AI endpoints
- [ ] Add retry/backoff for Anthropic API calls

## Milestone 4 — Payments (`Development`)
- [ ] `POST /api/checkout` — creates a $1 Stripe Checkout Session for generate/save/update
- [ ] `POST /api/webhook/stripe` — verifies Stripe signature, credits one action on `checkout.session.completed`
- [ ] Add idempotency handling on the webhook (Stripe can retry deliveries — don't double-credit)
- [ ] Add a credit-check dependency/middleware that gates generate/save/update endpoints
- [ ] `GET /api/credits` — returns current balance for the signed-in user

## Milestone 5 — Frontend integration (`Development`)
- [ ] Replace `window.claude.use("sample")` calls with `fetch()` to `/api/import` and `/api/check`
- [ ] Replace `window.claude.use("downloads")` with a normal `<a download>` / blob flow (works outside claude.ai)
- [ ] Add login/signup UI, tied to the backend auth endpoints
- [ ] Add a credit balance indicator + "$1 to continue" prompt before generate/save/update
- [ ] Wire the Stripe Checkout redirect into the UI flow

## Milestone 6 — Resume save/versioning (`Development`)
- [ ] `POST /api/resumes` — save a resume version tied to the signed-in user
- [ ] `GET /api/resumes` / `GET /api/resumes/{id}` — list and load saved resumes
- [ ] `PUT /api/resumes/{id}` — update, consuming one credit
- [ ] Add "my resumes" view in the frontend to list/reopen saved versions

## Milestone 7 — Testing (`Testing`)
- [ ] Unit tests for the credits ledger (no double-spend, no double-credit on webhook retries)
- [ ] Integration test: full flow — pay → generate → save → update, in Stripe test mode
- [ ] Test AI endpoints with malformed/huge input (don't trust the client)
- [ ] Cross-browser check of the frontend (Chrome, Safari, Firefox, mobile)
- [ ] Load-test the webhook endpoint (Stripe expects a fast 200 response)

## Milestone 8 — Deployment (`Testing` → `main`)
- [ ] Deploy backend (Render or Railway), set production env vars/secrets
- [ ] Deploy frontend (Vercel/Netlify, or served as static files from the same backend)
- [ ] Point custom domain at the deployment, confirm SSL
- [ ] Switch Stripe from test mode to live mode, update webhook URL in Stripe dashboard
- [ ] Set up error monitoring (Sentry) and uptime checks

## Milestone 9 — Launch prep (`main`)
- [ ] Write Terms of Service and Privacy Policy (you're storing PII — resumes, emails)
- [ ] Add a pricing/landing page explaining the $1 model
- [ ] Add basic analytics (signups, conversions, generate/save/update usage)
- [ ] Decide and document a data-retention/deletion policy for saved resumes
- [ ] Soft launch to a small group before public announcement

---

### Turning this into GitHub Issues
- **Manual**: copy each `- [ ]` line as an issue title, its `##` phase as a milestone or label.
- **Scripted**: if you have the `gh` CLI installed and authenticated, a loop like this bulk-creates issues from a milestone:
  ```bash
  gh issue create --title "Scaffold FastAPI app with /health endpoint" --milestone "Backend foundation" --label "backend"
  ```
  I can generate the full set of `gh issue create` commands for every task above if that's useful.
