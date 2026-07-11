from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework import generics
from rest_framework.response import Response
from .models import User, Project
from .serializers import UserSerializer, ProjectSerializer, ProjectHealthSerializer
from .health import refresh_stale_throttled, monitored_projects


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
