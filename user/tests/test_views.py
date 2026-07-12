from unittest.mock import patch
from django.core.cache import cache
from rest_framework.throttling import ScopedRateThrottle
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
from user.models import User, Project
from user import views as user_views
from user.views import SingletonUserView, ProjectListView, ProjectHealthView, HealthView
from user.tests.utils import create_sample_user, create_sample_file


def make_project(title, index, hidden=False, health_url=""):
    project = Project.objects.create(
        index=index, hidden=hidden, title=title,
        description="desc", image=create_sample_file(),
    )
    if health_url:
        project.healthUrl = health_url
        project.save()
    return project


class HealthViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        # Force a recompute (the verdict is cached across requests).
        user_views._health_cache['ok'] = None

    def test_healthy_returns_200_ok(self):
        response = HealthView.as_view()(self.factory.get(reverse('health')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['components']['database']['status'], 'ok')
        self.assertIn('uptimeSeconds', response.data)
        self.assertIn('timestamp', response.data)
        self.assertEqual(response['Cache-Control'], 'no-store')

    def test_degraded_returns_503_when_database_down(self):
        with patch('user.views._check_database', return_value=False):
            response = HealthView.as_view()(self.factory.get(reverse('health')))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.data['status'], 'degraded')
        self.assertEqual(response.data['components']['database']['status'], 'down')


class SingletonUserViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_sample_user()

    def test_get_user_success(self):
        url = reverse('singleton-user')
        request = self.factory.get(url)
        view = SingletonUserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_found(self):
        User.objects.all().delete()  # Remove the user created in setUp
        url = reverse('singleton-user')
        request = self.factory.get(url)
        view = SingletonUserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'User not found.'})


class ProjectListViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()  # isolate rate-limit counters between tests

    def test_list_returns_visible_projects_ordered_by_index(self):
        make_project("B", index=20)
        make_project("A", index=10)
        make_project("C", index=30)

        response = ProjectListView.as_view()(self.factory.get(reverse('projects')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([p['title'] for p in response.data], ['A', 'B', 'C'])

    def test_list_excludes_hidden_projects(self):
        make_project("Visible", index=10)
        make_project("Hidden", index=20, hidden=True)

        response = ProjectListView.as_view()(self.factory.get(reverse('projects')))
        self.assertEqual([p['title'] for p in response.data], ['Visible'])

    def test_list_is_side_effect_free(self):
        # The content endpoint must never trigger a health refresh.
        make_project("Visible", index=10)
        with patch('user.views.refresh_stale_throttled') as refresh:
            ProjectListView.as_view()(self.factory.get(reverse('projects')))
        refresh.assert_not_called()


class ProjectHealthViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()  # isolate rate-limit counters between tests

    @override_settings(PROJECT_HEALTH_LAZY_REFRESH=False)
    def test_returns_only_monitored_visible_projects(self):
        monitored = make_project("Monitored", index=10, health_url="https://svc/health")
        make_project("NoUrl", index=20)
        make_project("Hidden", index=30, hidden=True, health_url="https://svc/health")

        response = ProjectHealthView.as_view()(self.factory.get(reverse('projects-health')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row['id'] for row in response.data], [monitored.id])
        self.assertEqual(set(response.data[0].keys()), {'id', 'healthUp', 'healthCheckedAt'})

    @override_settings(PROJECT_HEALTH_LAZY_REFRESH=True, PROJECT_HEALTH_MAX_AGE=600)
    def test_triggers_lazy_refresh_when_enabled(self):
        make_project("Monitored", index=10, health_url="https://svc/health")
        with patch('user.views.refresh_stale_throttled') as refresh:
            ProjectHealthView.as_view()(self.factory.get(reverse('projects-health')))
        refresh.assert_called_once_with(600)

    @override_settings(PROJECT_HEALTH_LAZY_REFRESH=False)
    def test_does_not_trigger_refresh_when_disabled(self):
        make_project("Monitored", index=10, health_url="https://svc/health")
        with patch('user.views.refresh_stale_throttled') as refresh:
            ProjectHealthView.as_view()(self.factory.get(reverse('projects-health')))
        refresh.assert_not_called()

    @override_settings(PROJECT_HEALTH_LAZY_REFRESH=False, PROJECT_HEALTH_CLIENT_TTL=60)
    def test_response_is_cacheable_for_clients(self):
        make_project("Monitored", index=10, health_url="https://svc/health")
        response = ProjectHealthView.as_view()(self.factory.get(reverse('projects-health')))
        self.assertIn('max-age=60', response['Cache-Control'])

    @override_settings(PROJECT_HEALTH_LAZY_REFRESH=False)
    def test_health_endpoint_is_rate_limited(self):
        make_project("Monitored", index=10, health_url="https://svc/health")
        view = ProjectHealthView.as_view()
        # THROTTLE_RATES is import-bound, so patch the dict rather than settings.
        with patch.dict(ScopedRateThrottle.THROTTLE_RATES, {'health': '2/min'}):
            self.assertEqual(view(self.factory.get(reverse('projects-health'))).status_code, 200)
            self.assertEqual(view(self.factory.get(reverse('projects-health'))).status_code, 200)
            # Third call within the window is rejected.
            self.assertEqual(view(self.factory.get(reverse('projects-health'))).status_code, 429)
