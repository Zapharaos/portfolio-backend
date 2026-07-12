# Portfolio Backend

Django + Django REST Framework backend that powers the portfolio at
[matthieu-freitag.com](https://www.matthieu-freitag.com/). It exposes a small,
public, read‑only API consumed by the Vue front‑end, and everything is edited
through the Django admin — no code changes needed to update the site's content.

## What it does

- **Content API** — a single `GET /user/` returns the whole site (hero, about,
  work items, experiences, footer, socials, active theme). `GET /projects/`
  serves the full projects catalogue for the dedicated projects page.
- **Theming** — a `Theme` (3 CSS tokens) linked to the user re‑skins the whole
  front‑end; no theme = the front‑end defaults.
- **Project health badges** — each project can expose a health endpoint that the
  backend probes periodically; the front‑end shows a green/red "Live" dot.
- **Service liveness** — `GET /health/` for uptime monitors (200 / 503).

## At a glance

| Endpoint | Purpose |
|---|---|
| `GET /user/` | Whole site content (hidden items filtered out) |
| `GET /projects/` | All visible projects, ordered by `index` |
| `GET /projects/health/` | Per‑project health state (`healthUp`) |
| `GET /health/` | This service's own liveness |
| `/admin/` | Django admin — edit everything |

See the [API reference](api.md) for payloads and the [Data model](models.md) for
every editable field.

## Tech

- Python 3.12 · Django 5.0 · Django REST Framework 3.15
- SQLite (file‑based) · Gunicorn · Nginx · Docker Compose
- No `requests` dependency — health probes use the standard library
  (`urllib`).

## Where to go next

- [Getting started](getting-started.md) — run it locally, create an admin.
- [Configuration](configuration.md) — every environment variable.
- [Health checks](health-checks.md) — how the project health system works.
- [Deployment](deployment.md) — production with Docker + Nginx.
