# Deployment

Production runs Gunicorn behind Nginx, in Docker Compose.

## Docker Compose

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

The `portfolio-backend` service runs:

```
gunicorn portfolio-backend.wsgi:application --bind 0.0.0.0:${DJANGO_PORT} --workers 3
```

!!! important "Why `--workers 3`"
    Several workers let the server serve **its own** health probe. With a single
    worker, a project whose `healthUrl` points back at this backend deadlocks the
    probe (the only worker is busy handling `/projects/health/`). See
    [Health checks](health-checks.md).

The container mounts the project directory and joins the external
`vps-network`. `entrypoint.sh` runs `collectstatic` + `migrate` on start.

## Nginx

`nginx.conf` (see `example.nginx.conf`) terminates TLS and proxies:

- `api.<domain>` → `http://portfolio-backend:8001/` (everything, including
  `/media/`, so DRF's `request` builds **absolute** media URLs and CORS headers
  are applied).
- `/static` → the collected static files.

!!! warning "Media must be absolute & same‑origin‑served"
    The API returns absolute media URLs (`https://api…/media/…`). The front‑end
    lives on a different origin, so relative URLs would 404. This works because
    media is proxied through Django (which sets the host and CORS headers). If
    you serve `/media` directly from Nginx, add CORS headers there.

## Migrations

Applied automatically by `entrypoint.sh` on container start. To run manually:

```bash
docker compose -f docker-compose.prod.yml exec portfolio-backend python manage.py migrate
```

Deploy after any model change (new fields ship as migrations).

## Continuous integration

`.github/workflows/ci.yaml` runs flake8, the test suite with coverage, and
uploads to Codecov on pushes/PRs to `main` and `develop`.

## Documentation site

`.github/workflows/docs.yml` builds this MkDocs site and deploys it to GitHub
Pages on every push to `main` that touches the docs. Enable it once under
**Settings → Pages → Source: GitHub Actions**.
