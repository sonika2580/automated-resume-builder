# Backend

FastAPI app for DollarResume.

## Set up Supabase

1. Create a free project at [supabase.com](https://supabase.com)
2. In **Project Settings → Data API**, copy the **Project URL** and **anon public key** →
   these go in `SUPABASE_URL` and `SUPABASE_ANON_KEY`
3. In **Project Settings → Database → Connection string**, copy the URI (use the "Session
   pooler" connection for serverless-friendly hosting, or the direct connection for local
   dev) → this goes in `DATABASE_URL`
4. Under **Authentication → Providers**, email sign-up is on by default — that's enough to
   test with; add OAuth providers later if you want them

Supabase manages its own `auth.users` table for you. Our app's own tables (resumes,
credits_ledger, payments) are created by the Alembic migration below, in the same database.

## Run locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env   # then fill in real values, including the Supabase ones above
alembic upgrade head          # creates resumes / credits_ledger / payments tables
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/health` — you should see `{"status": "ok", "billing_enabled": false}`.
Interactive API docs are at `http://localhost:8000/docs`.

To check the auth flow: sign a user up via Supabase (e.g. through their client SDK on the
frontend, or the Supabase dashboard), take the `access_token` from that session, and call:

```bash
curl http://localhost:8000/api/me -H "Authorization: Bearer <access_token>"
```

You should get back `{"id": ..., "email": ..., "credits": 0}`.

## Run tests

```bash
pytest
```

## Layout

```
app/
  main.py              FastAPI app, CORS, router registration
  config.py             Settings loaded from environment (.env)
  logging_config.py     Logging setup
  db.py                  SQLAlchemy engine/session
  models.py              Resume, CreditLedgerEntry, Payment
  deps.py                 get_current_user — verifies the Supabase session token
  services/
    credits.py            Credit balance + ledger helpers
  routers/
    health.py             Liveness check
    users.py                GET /api/me — profile + credit balance          ✅ live
    resumes.py              Save/load/update resumes                        — Milestone 6
    ai.py                    Import + resume checker endpoints                ✅ live (needs ANTHROPIC_API_KEY)
    billing.py               Stripe checkout + webhook                        — Milestone 4
  services/
    extraction.py            PDF/DOCX text extraction (pdfplumber, python-docx)
    claude.py                 Thin wrapper for JSON-structured Anthropic API calls
migrations/
  versions/0001_initial.py  Creates resumes / credits_ledger / payments tables
tests/
  test_health.py
  test_ai.py
```

`resumes.py` and `billing.py` still return `501 Not Implemented`. `ai.py` is fully live —
set `ANTHROPIC_API_KEY` in `.env` and try it:

```bash
curl -X POST http://localhost:8000/api/import -F "file=@/path/to/resume.pdf"

curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{"name":"Jordan Ellis","experience":[{"company":"Acme","role":"Engineer","bullets":"Built things"}]}'
```

