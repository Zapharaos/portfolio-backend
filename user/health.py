"""Project health-check logic, shared by the management command (manual/periodic)
and the dedicated health endpoint (synchronous, TTL-throttled, parallel probes)."""

import socket
import threading
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

# Consecutive failures required before the badge flips to "down". Guards against
# transient blips (a single timed-out check won't take a project offline).
FAILURE_THRESHOLD = 2

# Per-probe GET timeout, in seconds. Probes run in parallel, so the whole refresh
# is bounded by (roughly) this timeout, not timeout × number of projects.
PROBE_TIMEOUT = 5

# Ensures a single throttled refresh runs at a time per process (avoids two
# concurrent requests both probing the same stale services).
_refresh_lock = threading.Lock()


def probe(url):
    """Return True when the endpoint is alive (any HTTP status < 500, incl. 429).
    5xx, timeouts and connection/DNS/TLS errors count as down. Never raises."""
    request = urllib.request.Request(url, headers={'User-Agent': 'portfolio-healthcheck'})
    try:
        with urllib.request.urlopen(request, timeout=PROBE_TIMEOUT) as response:
            return response.status < 500
    except urllib.error.HTTPError as error:
        # 4xx (incl. 429 rate-limited) means the service is up; 5xx is down.
        return error.code < 500
    except (urllib.error.URLError, TimeoutError, socket.timeout):
        return False
    except Exception:  # noqa: BLE001 - never let one project crash the run
        return False


def _apply_result(project, ok):
    """Persist a probe result on a project (failure streak / up-down transition)."""
    if ok:
        project.healthFailures = 0
        project.healthUp = True
    else:
        project.healthFailures += 1
        # Stay in the previous state until the failure streak is confirmed.
        if project.healthFailures >= FAILURE_THRESHOLD:
            project.healthUp = False
    project.healthCheckedAt = timezone.now()
    project.save(update_fields=['healthUp', 'healthCheckedAt', 'healthFailures'])


def monitored_projects():
    """Projects that opted into monitoring (non-empty healthUrl)."""
    from user.models import Project
    return Project.objects.exclude(healthUrl__isnull=True).exclude(healthUrl='')


def refresh_project(project):
    """Probe a single project and persist its state. Returns the probe result."""
    ok = probe(project.healthUrl)
    _apply_result(project, ok)
    return ok


def refresh_projects(projects):
    """Probe the given projects in parallel, then persist results. Returns the
    number of projects refreshed. DB writes happen in this thread (probes only
    are parallelised), so there is no cross-thread DB access."""
    projects = list(projects)
    if not projects:
        return 0
    max_workers = min(settings.PROJECT_HEALTH_MAX_WORKERS, len(projects))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda p: (p, probe(p.healthUrl)), projects))
    for project, ok in results:
        _apply_result(project, ok)
    return len(results)


def _stale(max_age_seconds):
    cutoff = timezone.now() - timedelta(seconds=max_age_seconds)
    return monitored_projects().filter(
        models.Q(healthCheckedAt__isnull=True) | models.Q(healthCheckedAt__lt=cutoff)
    )


def refresh_stale(max_age_seconds):
    """Re-probe monitored projects whose last check is older than the TTL (or
    never checked). Returns the number of projects refreshed."""
    return refresh_projects(_stale(max_age_seconds))


def refresh_stale_throttled(max_age_seconds):
    """TTL-throttled refresh, safe to call on every request: probes only the
    stale projects, and only one refresh runs at a time (concurrent callers get
    the current stored state instead of re-probing). Returns projects refreshed."""
    if not _refresh_lock.acquire(blocking=False):
        return 0
    try:
        return refresh_stale(max_age_seconds)
    finally:
        _refresh_lock.release()
