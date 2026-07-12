# Health checks

Two independent things share the word "health":

1. **Project health** — is an *external* project (whose `healthUrl` you set)
   responding? Drives the green/red "Live" dot on project cards.
2. **Service health** — is *this* backend alive? Exposed at `GET /health/` for
   uptime monitors.

## Project health

### Fields (on `Project`)

| Field | Meaning |
|---|---|
| `healthUrl` | Endpoint to probe. Empty = the project is never checked. |
| `healthUp` | `true` (up), `false` (confirmed down), `null` (never checked). |
| `healthCheckedAt` | Timestamp of the last probe. |
| `healthFailures` | Consecutive failures (anti‑false‑negative counter). |

Clearing `healthUrl` resets `healthUp` and `healthFailures` (the badge
disappears).

### Probe rules

A probe is **up** when the endpoint answers HTTP `< 500` (including `429`
rate‑limited = alive). It is **down** on `5xx`, timeouts, or DNS/connection/TLS
errors. Probes never raise — a broken endpoint can't interrupt the others.

- Timeout: `PROBE_TIMEOUT = 5s` per probe.
- Probes run **in parallel** (up to `PROJECT_HEALTH_MAX_WORKERS`, default 32), so
  a refresh is bounded to ~one timeout window even with many projects.

### Up / down transitions (anti‑flapping)

- A **success** sets `healthUp = true` and resets the failure counter — the badge
  recovers immediately.
- A **failure** increments the counter but only flips `healthUp = false` after
  **2 consecutive failures** (`FAILURE_THRESHOLD`). A single blip doesn't take a
  project offline.

### When does it run?

Only `GET /projects/health/` triggers a refresh, and only for **stale** projects
(last check older than `PROJECT_HEALTH_MAX_AGE`, default 600s). Within the TTL,
the endpoint returns the stored state without probing. This means:

- Reloading the page does **not** force a re‑probe — services are pinged at most
  once per TTL, whatever the traffic.
- Only one refresh runs at a time per process (a lock; concurrent callers get the
  stored state).

Set `PROJECT_HEALTH_LAZY_REFRESH=false` to disable on‑access refresh and rely
solely on the management command.

### Force a refresh manually

```bash
python manage.py check_project_health
```

Runs in a separate process, ignores the TTL, and probes every monitored project.
Handy to test after setting a `healthUrl`.

!!! warning "Self‑monitoring needs several workers"
    If a project's `healthUrl` points at **this** backend (e.g. its own
    `/health/`), a single‑worker Gunicorn deadlocks: the worker handling
    `/projects/health/` can't serve its own probe → timeout → failure. Run
    Gunicorn with `--workers 3` (see [Deployment](deployment.md)). The
    management command has no such issue (separate process).

## Service health (`/health/`)

`GET /health/` (and `HEAD`) returns this service's liveness:

```json
{ "status": "ok", "uptimeSeconds": 1234, "timestamp": "…", "components": { "database": { "status": "ok" } } }
```

- `200` when healthy, `503` + `"status": "degraded"` when the database is
  unreachable — so a monitor treating non‑2xx as "down" works out of the box.
- The dependency probe is cached ~5s to stay cheap under frequent polling;
  `Cache-Control: no-store`.
- Set `APP_VERSION` to include a `version` field.

You can even point the portfolio project's own `healthUrl` at
`https://api.yourdomain.com/health/` so it self‑reports in the projects list.
