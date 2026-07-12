import os
import threading
import time
from datetime import datetime, timezone

from django.conf import settings
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Project
from .serializers import UserSerializer, ProjectSerializer, ProjectHealthSerializer
from .health import refresh_stale_throttled, monitored_projects


# --- Service health (this backend's own liveness, for uptime monitors) --------
# Distinct from ProjectHealthView, which reports the state of *external* projects.

_STARTED_AT = time.monotonic()
_HEALTH_CACHE_TTL = 5  # seconds — bound how often we actually probe dependencies
_health_lock = threading.Lock()
_health_cache = {'at': 0.0, 'ok': None, 'components': None}


def _check_database():
    """True when the database answers a trivial query."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return True
    except Exception:  # noqa: BLE001
        return False


def _compute_health():
    db_ok = _check_database()
    components = {'database': {'status': 'ok' if db_ok else 'down'}}
    # The database is critical: if it's down the API can't serve → degraded.
    return db_ok, components


class HealthView(APIView):
    """Public liveness endpoint for uptime monitors / a status widget.

    Returns 200 + `{"status": "ok", ...}` when healthy, 503 + `"degraded"` when a
    critical dependency (the database) is down, so any monitor treating non-2xx
    as "down" works out of the box. Dependency probes are cached briefly to stay
    cheap under frequent polling. Not rate-limited (monitors poll often)."""

    def get(self, request, *args, **kwargs):
        now = time.monotonic()
        with _health_lock:
            if _health_cache['ok'] is None or now - _health_cache['at'] > _HEALTH_CACHE_TTL:
                ok, components = _compute_health()
                _health_cache.update(at=now, ok=ok, components=components)
            ok, components = _health_cache['ok'], _health_cache['components']

        payload = {
            'status': 'ok' if ok else 'degraded',
            'uptimeSeconds': int(time.monotonic() - _STARTED_AT),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'components': components,
        }
        version = os.environ.get('APP_VERSION')
        if version:
            payload['version'] = version

        response = Response(payload, status=200 if ok else 503)
        response['Cache-Control'] = 'no-store'
        return response

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class SingletonUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    throttle_scope = 'user'

    def get_object(self):
        return User.objects.first()

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        return Response({"detail": "User not found."}, status=404)


class ProjectListView(generics.ListAPIView):
    """All visible projects, ordered by index — feeds the dedicated projects page.

    Pure content: no health, no side effects, cacheable. Health is served by
    ProjectHealthView and merged client-side by `id`."""
    serializer_class = ProjectSerializer
    throttle_scope = 'projects'

    def get_queryset(self):
        return Project.objects.filter(hidden=False).order_by('index')


@method_decorator(
    cache_control(public=True, max_age=settings.PROJECT_HEALTH_CLIENT_TTL),
    name='dispatch',
)
class ProjectHealthView(generics.ListAPIView):
    """Health state of the monitored (visible) projects.

    Being a dedicated call (the frontend fetches it after the content), it can
    afford to wait: it synchronously re-probes stale services (TTL-throttled,
    probes run in parallel) and returns fresh state. The TTL bounds how often
    services are actually pinged, regardless of traffic. Rate-limited per IP and
    marked cacheable for PROJECT_HEALTH_CLIENT_TTL seconds so clients reuse a
    fresh result instead of refetching."""
    serializer_class = ProjectHealthSerializer
    throttle_scope = 'health'

    def get_queryset(self):
        if settings.PROJECT_HEALTH_LAZY_REFRESH:
            refresh_stale_throttled(settings.PROJECT_HEALTH_MAX_AGE)
        return monitored_projects().filter(hidden=False).order_by('index')
