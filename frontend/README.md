# Frontend

A single self-contained `index.html` — no build step, no framework, no npm install.

## Run locally

Just open `index.html` in a browser, or serve it with anything static:

```bash
cd frontend
python3 -m http.server 5500
# visit http://localhost:5500
```

Make sure the backend is running too (see `../backend/README.md`) — the import and resume
checker features call it directly.

## Pointing it at your backend

By default the page calls `http://localhost:8000/api`. If you're running the backend
somewhere else, set this before `index.html`'s own script runs — either add a small inline
script above it, or edit the constant directly:

```html
<script>window.DOLLARRESUME_API_BASE = "https://api.yourdomain.com/api";</script>
```

Also make sure that origin is listed in the backend's `CORS_ORIGINS` setting
(`backend/app/config.py`), or the browser will block the requests.

## What's wired up vs. what isn't yet

- ✅ Live resume builder with autosave (browser localStorage)
- ✅ Import from PDF/DOCX/TXT → calls `POST /api/import`
- ✅ AI resume checker with approvable suggested edits → calls `POST /api/check`
- ✅ Print-to-PDF via the browser's print dialog
- ⏳ Login/signup UI and the "$1 to continue" credit prompt aren't built yet — the backend's
  `/api/me`, `/api/resumes`, and billing endpoints exist, but nothing here calls them. That's
  the next piece of work (see the project task breakdown for what's tracked).
