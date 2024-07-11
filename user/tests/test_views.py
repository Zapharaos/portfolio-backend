import re
from django.test import TestCase, RequestFactory
from django.urls import reverse
from user.models import User
from user.serializers import UserSerializer
from user.views import SingletonUserView
from user.tests.utils import create_sample_user


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
