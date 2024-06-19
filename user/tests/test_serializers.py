from django.test import TestCase
from user.models import User, List
from user.serializers import (
    SocialSerializer,
    ListItemSerializer,
    ListSerializer,
    ThemeSerializer,
    UserSerializer,
)


class SocialSerializerTests(TestCase):

    def test_social_serializer_fields(self):
        serializer = SocialSerializer(data={'name': 'Test', 'url': 'https://www.test.com/', 'hidden': False})
        self.assertEqual(set(serializer.fields.keys()), {'name', 'url', 'hidden'})
        self.assertTrue(serializer.is_valid())


class ListSerializerTests(TestCase):

    def test_list_serializer_fields_and_nested_serializer(self):
        user = User.objects.create(hero="Test User", email="test@email.com")
        serializer = ListSerializer(List.objects.create(idUser=user, name="List 1", index=1))
        self.assertEqual(set(serializer.fields.keys()), {'name', 'index', 'hidden', 'items'})


class ListItemSerializerTests(TestCase):

    def test_list_item_serializer_fields(self):
        serializer = ListItemSerializer(data={
            'index': 1,
            'organisation': 'Test Org',
            'name': 'Item Name',
            'menuName': 'Menu Item',
            'address': '123 Main St',
            'period': '2020-2021',
            'description': 'This is a description',
            'hidden': False,
        })
        self.assertEqual(set(serializer.fields.keys()),
                         {'index', 'organisation', 'name', 'menuName', 'address', 'period', 'description', 'hidden'})
        self.assertTrue(serializer.is_valid())


class ThemeSerializerTests(TestCase):

    def test_theme_serializer_fields(self):
        serializer = ThemeSerializer(data={'name': 'Light Theme', 'todo': '#FFFFFF'})
        self.assertEqual(set(serializer.fields.keys()), {'name', 'todo'})
        self.assertTrue(serializer.is_valid())


class UserSerializerTests(TestCase):

    def test_user_serializer_fields_and_nested_serializers(self):
        user = User.objects.create(hero="Test User", email="test@email.com")
        serializer = UserSerializer(user)
        self.assertEqual(set(serializer.fields.keys()),
                         {'id', 'hero', 'description', 'email', 'logo', 'photo', 'curriculum', 'socials', 'lists',
                          'theme_light', 'theme_dark'})
