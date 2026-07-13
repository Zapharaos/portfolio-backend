#!/usr/bin/env bash
#
# Backup the portfolio's persistent data: the SQLite database (which holds ALL
# site content) and the uploaded media/. Produces one timestamped .tar.gz and
# prunes old ones. Meant to run from cron on the VPS.
#
# Override paths via env vars if your layout differs:
#   APP_DIR         where db.sqlite3 and media/ live (the bind-mount source)
#   BACKUP_DIR      where archives are written (ideally another disk / offsite)
#   RETENTION_DAYS  how many days of backups to keep
#
# Example cron (daily at 03:00):
#   0 3 * * * /home/dev/matthieu/portfolio/back/scripts/backup.sh >> /var/log/portfolio-backup.log 2>&1

set -euo pipefail

APP_DIR="${APP_DIR:-/home/dev/matthieu/portfolio/back}"
BACKUP_DIR="${BACKUP_DIR:-/home/dev/matthieu/portfolio/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"

timestamp="$(date +%Y%m%d-%H%M%S)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

mkdir -p "$BACKUP_DIR"

# Consistent SQLite snapshot — safe even while the app is writing (unlike a raw
# cp, which can catch a half-written state). Falls back to cp if sqlite3 is absent.
if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 "$APP_DIR/db.sqlite3" ".backup '$work/db.sqlite3'"
else
  echo "warning: sqlite3 not found, using cp (less safe under concurrent writes)" >&2
  cp "$APP_DIR/db.sqlite3" "$work/db.sqlite3"
fi

# Uploaded media (skip gracefully if empty/missing).
if [ -d "$APP_DIR/media" ]; then
  cp -a "$APP_DIR/media" "$work/media"
else
  mkdir -p "$work/media"
fi

archive="$BACKUP_DIR/portfolio-$timestamp.tar.gz"
tar -czf "$archive" -C "$work" db.sqlite3 media
echo "Backup written: $archive ($(du -h "$archive" | cut -f1))"

# Prune backups older than the retention window.
find "$BACKUP_DIR" -maxdepth 1 -name 'portfolio-*.tar.gz' -type f -mtime "+$RETENTION_DAYS" -delete
