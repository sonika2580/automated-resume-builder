# Backend

FastAPI app for DollarResume.

## Run locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env   # then fill in real values
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/health` — you should see `{"status": "ok", "billing_enabled": false}`.
Interactive API docs are at `http://localhost:8000/docs` (FastAPI generates these automatically).

## Run tests

```bash
pytest
```

## Layout

```
app/
  main.py            FastAPI app, CORS, router registration
  config.py           Settings loaded from environment (.env)
  logging_config.py   Logging setup
  deps.py              Shared dependencies (auth placeholder for now)
  routers/
    health.py         Liveness check
    resumes.py         Save/load/update resumes            — Milestone 6
    ai.py               Import + resume checker endpoints    — Milestone 3
    billing.py          Stripe checkout + webhook             — Milestone 4
tests/
  test_health.py
```

Routers other than `health` currently return `501 Not Implemented` — that's intentional.
The structure is in place; the logic behind each fills in milestone by milestone (see the
project task breakdown for what's next).
