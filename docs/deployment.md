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

## Persistence & media

`db.sqlite3` and `media/` live on the host via the compose bind‑mount
(`.:/usr/src/app/`) — **without a volume/mount they are ephemeral** and reset on
every rebuild. `.dockerignore` also keeps them out of the image, so old uploads
never resurrect on redeploy. See [Media & files](media.md) for storage, the
`clean_orphan_media` command and the CDN‑cache caveat.

Confirm the mount is active:

```bash
docker inspect portfolio-backend --format '{{json .Mounts}}'
```

## Backups

`db.sqlite3` holds **all** the site's content, so back it up (and `media/`).
[`scripts/backup.sh`](https://github.com/Zapharaos/portfolio-backend/blob/main/scripts/backup.sh)
writes a single timestamped `.tar.gz` (a consistent SQLite snapshot via
`sqlite3 .backup` + the media folder) and prunes old ones.

```bash
chmod +x scripts/backup.sh          # once

# Run it (paths overridable via APP_DIR / BACKUP_DIR / RETENTION_DAYS)
./scripts/backup.sh
```

Schedule it with cron (daily at 03:00):

```cron
0 3 * * * /home/dev/matthieu/portfolio/back/scripts/backup.sh >> /var/log/portfolio-backup.log 2>&1
```

Restore:

```bash
tar -xzf portfolio-YYYYMMDD-HHMMSS.tar.gz -C /home/dev/matthieu/portfolio/back
docker compose -f docker-compose.prod.yml restart portfolio-backend
```

!!! tip
    Store backups on a different disk or off‑site — a backup next to the data it
    protects doesn't survive a disk loss.

## Security hardening

Django sits behind Nginx (TLS). `settings.py` sets:

- `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` so Django knows
  requests are HTTPS.
- `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` = `True` when `DEBUG` is off, so
  the admin's session/CSRF cookies are only sent over HTTPS.

Also make sure production env has `DJANGO_DEBUG_MODE=False` (or unset), a strong
`DJANGO_SECRET_KEY`, and correct `DJANGO_ALLOWED_HOSTS`.

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
