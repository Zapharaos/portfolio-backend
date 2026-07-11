import socket
import urllib.error
from datetime import timedelta
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from user import health
from user.models import Project
from user.tests.utils import create_sample_file

PROBE = 'user.health.probe'


def make_project(title="P", health_url="https://svc.example/health"):
    project = Project.objects.create(
        index=1, hidden=False, url="https://project.com", title=title,
        description="desc", image=create_sample_file(),
    )
    if health_url:
        project.healthUrl = health_url
        project.save()
    return project


class CheckProjectHealthCommandTests(TestCase):

    def test_success_sets_up_and_resets_failures(self):
        project = make_project()
        project.healthFailures = 5
        project.save()
        with patch(PROBE, return_value=True):
            call_command('check_project_health')
        project.refresh_from_db()
        self.assertTrue(project.healthUp)
        self.assertEqual(project.healthFailures, 0)
        self.assertIsNotNone(project.healthCheckedAt)

    def test_single_failure_keeps_previous_state(self):
        project = make_project()
        project.healthUp = True
        project.save()
        with patch(PROBE, return_value=False):
            call_command('check_project_health')
        project.refresh_from_db()
        self.assertTrue(project.healthUp)
        self.assertEqual(project.healthFailures, 1)

    def test_two_consecutive_failures_flip_to_down(self):
        project = make_project()
        project.healthUp = True
        project.save()
        with patch(PROBE, return_value=False):
            call_command('check_project_health')
            call_command('check_project_health')
        project.refresh_from_db()
        self.assertFalse(project.healthUp)
        self.assertEqual(project.healthFailures, 2)

    def test_success_after_failure_restores_up_immediately(self):
        project = make_project()
        project.healthUp = False
        project.healthFailures = 4
        project.save()
        with patch(PROBE, return_value=True):
            call_command('check_project_health')
        project.refresh_from_db()
        self.assertTrue(project.healthUp)
        self.assertEqual(project.healthFailures, 0)

    def test_projects_without_health_url_are_not_probed(self):
        make_project(title="NoUrl", health_url="")
        with patch(PROBE, return_value=True) as probe:
            call_command('check_project_health')
        probe.assert_not_called()


class ProbeTests(TestCase):

    def test_probe_returns_false_on_network_error(self):
        with patch('urllib.request.urlopen', side_effect=urllib.error.URLError('boom')):
            self.assertFalse(health.probe('https://svc.example/health'))
        with patch('urllib.request.urlopen', side_effect=socket.timeout()):
            self.assertFalse(health.probe('https://svc.example/health'))

    def test_probe_treats_429_as_up(self):
        err = urllib.error.HTTPError('u', 429, 'Too Many Requests', {}, None)
        with patch('urllib.request.urlopen', side_effect=err):
            self.assertTrue(health.probe('https://svc.example/health'))

    def test_probe_treats_500_as_down(self):
        err = urllib.error.HTTPError('u', 503, 'Service Unavailable', {}, None)
        with patch('urllib.request.urlopen', side_effect=err):
            self.assertFalse(health.probe('https://svc.example/health'))


class RefreshStaleTests(TestCase):

    def test_refreshes_never_checked_projects(self):
        project = make_project()
        with patch(PROBE, return_value=True):
            refreshed = health.refresh_stale(max_age_seconds=600)
        project.refresh_from_db()
        self.assertEqual(refreshed, 1)
        self.assertTrue(project.healthUp)

    def test_skips_recently_checked_projects(self):
        project = make_project()
        project.healthCheckedAt = timezone.now()
        project.healthUp = True
        project.save()
        with patch(PROBE, return_value=False) as probe:
            refreshed = health.refresh_stale(max_age_seconds=600)
        probe.assert_not_called()
        self.assertEqual(refreshed, 0)

    def test_refreshes_projects_past_the_ttl(self):
        project = make_project()
        project.healthCheckedAt = timezone.now() - timedelta(seconds=1200)
        project.healthUp = True
        project.save()
        with patch(PROBE, return_value=True) as probe:
            refreshed = health.refresh_stale(max_age_seconds=600)
        probe.assert_called_once()
        self.assertEqual(refreshed, 1)
