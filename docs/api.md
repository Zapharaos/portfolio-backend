# API reference

All endpoints are **public** and **read‑only** (`GET`). They are meant to be
consumed by the front‑end, so everything returned is content that already
appears on the public site. There is no authentication.

!!! info "Trailing slash"
    URLs use a trailing slash. `/user` → `301` → `/user/`. Clients (and the
    health probe) follow the redirect, but prefer the canonical form.

## `GET /user/`

Returns the whole site as one document: the singleton user plus every nested
section. **Hidden items are filtered out** server‑side (hidden work items,
projects, experiences and socials never appear), and collections are ordered by
`index`.

- `200` with the payload, or `404 {"detail": "User not found."}` if no user
  exists yet.
- Rate limit: `user` scope (default **60/min** per IP).

```json
{
  "name": "…",
  "email": "…",
  "location": "…",
  "locale": "fr-FR",
  "timezone": "Europe/Paris",
  "logo": { "name": "…", "file": "https://api…/media/logo.png", "creditsUrl": null, "creditsShortUrl": null },
  "resume": { "…": "…" },
  "socials": [ { "index": 0, "hidden": false, "name": "GitHub", "pseudo": "…", "url": "…", "image": { "…": "…" } } ],
  "theme": { "name": "Ocean", "background": "#0b1622", "text": "#eaf2ff", "primary": "#00add8" },
  "hero": { "title": "…", "tagline": "…", "callToActionContent": "…", "backgroundImage": { "…": "…" } },
  "about": { "image": { "…": "…" }, "imageResponsive": { "…": "…" }, "description": "…" },
  "work": { "items": [ { "index": 0, "hidden": false, "title": "Projects", "projects": [ … ], "experiences": [ … ], "showProjects": true, "showExperiences": false } ] },
  "footer": { "title": "…", "subTitle": "…", "showLocation": true, "showSocials": true, "showEmail": true, "showResume": true }
}
```

`theme` is `null` when no theme is linked. Media URLs (`file`) are **absolute**
so the front‑end can load them from a different origin.

## `GET /projects/`

The full catalogue of **visible** projects (`hidden = false`), ordered by
`index`. This feeds the dedicated projects page. It carries **no health data**
and has **no side effects** (safe to cache). Health lives on its own endpoint
and is merged client‑side by `id`.

- Rate limit: `projects` scope (default **60/min** per IP).

```json
[
  {
    "id": 1,
    "index": 0,
    "hidden": false,
    "title": "BrickScanr",
    "description": "…",
    "category": "LEGO",
    "metric": "",
    "isNew": true,
    "inProgress": false,
    "iconFramed": true,
    "imageFit": "cover",
    "image": { "name": "…", "file": "https://api…/media/brickscanr.png", "creditsUrl": null, "creditsShortUrl": null },
    "technologies": [ { "name": "Go", "color": "#00ADD8" } ],
    "links": [
      { "kind": "github", "url": "https://github.com/…", "label": "GitHub", "icon": { "…": "…" }, "iconPosition": "before", "color": "#6e5494", "index": 0 }
    ]
  }
]
```

Field meanings are documented in the [Data model](models.md#project).

## `GET /projects/health/`

Per‑project health state for the **monitored, visible** projects (those with a
non‑empty `healthUrl`). The front‑end merges it into the projects by `id`.

- Synchronously re‑probes **stale** projects (older than the TTL), throttled so
  services are pinged at most once per TTL regardless of traffic.
- `Cache-Control: public, max-age=<PROJECT_HEALTH_CLIENT_TTL>` so clients reuse
  a fresh result instead of refetching.
- Rate limit: `health` scope (default **30/min** per IP).

```json
[
  { "id": 1, "healthUp": true, "healthCheckedAt": "2026-07-12T09:33:00Z" },
  { "id": 3, "healthUp": false, "healthCheckedAt": "2026-07-12T09:33:00Z" }
]
```

`healthUp` is `true` (up), `false` (confirmed down) or `null` (never checked).
See [Health checks](health-checks.md) for the full lifecycle.

## `GET /health/`  ·  `HEAD /health/`

This service's own liveness, for uptime monitors / a status widget. Distinct
from `/projects/health/`, which reports *external* projects.

- `200` + `"status": "ok"` when healthy, `503` + `"degraded"` when a critical
  dependency (the database) is down.
- `Cache-Control: no-store`. Not rate‑limited (monitors poll often); the
  dependency probe is cached internally for a few seconds.

```json
{
  "status": "ok",
  "uptimeSeconds": 1234,
  "timestamp": "2026-07-12T09:33:00+00:00",
  "components": { "database": { "status": "ok" } },
  "version": "1.4.0"
}
```

`version` is included only when the `APP_VERSION` env var is set.

## `/admin/`

The Django admin — the primary way to edit content. See
[Getting started](getting-started.md#create-an-admin-user).
