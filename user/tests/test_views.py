from django.test import TestCase, RequestFactory
from django.urls import reverse, path
from user.models import User
from user.serializers import UserSerializer
from user.views import SingletonUserView


class SingletonUserViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            hero='Test User',
            description='Description',
            email='test@email.com',
        )

    def test_get_user_success(self):
        url = reverse('singleton-user')
        request = self.factory.get(url)
        view = SingletonUserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_not_found(self):
        User.objects.all().delete()  # Remove the user created in setUp
        url = reverse('singleton-user')
        request = self.factory.get(url)
        view = SingletonUserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'User not found.'})
