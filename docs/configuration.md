# Configuration

All configuration is via environment variables (loaded from `.env`). Start from
`.env.dev` (development) or `.env.prod.example` (production).

## Django core

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key. **Required in production.** |
| `DJANGO_DEBUG_MODE` | `True` / `False`. |
| `DJANGO_ALLOWED_HOSTS` | Comma‑separated allowed hosts. |
| `DJANGO_PORT` | Port Gunicorn/dev server binds to (e.g. `8001`). |
| `CORS_ALLOWED_ORIGINS` | Comma‑separated front‑end origins allowed to call the API. |
| `CSRF_TRUSTED_ORIGINS` | Comma‑separated trusted origins for CSRF. |

## Rate limiting (DRF throttling)

Per‑IP throttles (scoped). Format is `<count>/<period>`, e.g. `30/min`.

| Variable | Default | Applies to |
|---|---|---|
| `THROTTLE_HEALTH` | `30/min` | `GET /projects/health/` |
| `THROTTLE_PROJECTS` | `60/min` | `GET /projects/` |
| `THROTTLE_USER` | `60/min` | `GET /user/` |

`GET /health/` is intentionally **not** throttled (uptime monitors poll it).

!!! note
    Throttle counters live in Django's cache. The default `LocMemCache` is
    **per process**, so with several Gunicorn workers each worker counts
    separately. For a strict shared limit, configure a shared cache (Redis /
    Memcached).

## Project health

| Variable | Default | Description |
|---|---|---|
| `PROJECT_HEALTH_LAZY_REFRESH` | `true` | Re‑probe stale projects on `GET /projects/health/`. Set `false` to rely only on the management command. |
| `PROJECT_HEALTH_MAX_AGE` | `600` | TTL (seconds): a project is re‑probed at most once per this window. |
| `PROJECT_HEALTH_MAX_WORKERS` | `32` | Max concurrent probes per refresh. |
| `PROJECT_HEALTH_CLIENT_TTL` | `60` | `Cache-Control: max-age` on the health response. |

See [Health checks](health-checks.md) for the behaviour.

## Misc

| Variable | Description |
|---|---|
| `APP_VERSION` | Optional. When set, `GET /health/` includes a `version` field. |

## Linting

`setup.cfg` configures flake8: `max-line-length = 119`, migrations excluded.
