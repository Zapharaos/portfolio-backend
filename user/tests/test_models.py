from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User, Theme, List, ListItem, Social


class ThemeModelTest(TestCase):
    def test_create_theme(self):
        theme = Theme.objects.create(name="Light", todo="#FFFFFF")
        self.assertEqual(theme.name, "Light")
        self.assertEqual(theme.todo, "#FFFFFF")

    def test_unique_name(self):
        Theme.objects.create(name="Light", todo="#FFFFFF")
        with self.assertRaises(ValidationError):
            theme = Theme(name="Light", todo="#000000")
            theme.full_clean()


class UserModelTests(TestCase):

    def test_unique_user(self):
        User.objects.create(hero="Some Hero", email="unique@email.com")
        with self.assertRaises(ValidationError):
            user = User.objects.create(hero="Another Hero", email="another@email.com")
            user.full_clean()

    def test_user_creation(self):
        theme_light = Theme.objects.create(name="Light", todo="#FFFFFF")
        theme_dark = Theme.objects.create(name="Dark", todo="#000000")
        User.objects.create(
            hero="Hero",
            description="Description",
            email="test@example.com",
            logo="path/to/logo.png",
            photo="path/to/photo.png",
            curriculum="path/to/curriculum.pdf",
            theme_light=theme_light,
            theme_dark=theme_dark
        )
        self.assertEqual(User.objects.count(), 1)


class SocialModelTest(TestCase):
    def test_create_social(self):
        user = User.objects.create(hero="Hero", description="Description", email="test@example.com")
        social = Social.objects.create(idUser=user, name="Test", url="https://test.com", hidden=False)
        self.assertEqual(social.name, "Test")
        self.assertEqual(social.url, "https://test.com")

    def test_unique_constraints(self):
        user = User.objects.create(hero="Hero", description="Description", email="test@example.com")
        Social.objects.create(idUser=user, name="Test", url="https://test.com", hidden=False)
        with self.assertRaises(ValidationError):
            social = Social(idUser=user, name="Test", url="https://test.com/another")
            social.full_clean()
        with self.assertRaises(ValidationError):
            social = Social(idUser=user, name="Test Another", url="https://test.com")
            social.full_clean()


class ListModelTest(TestCase):
    def test_create_list(self):
        user = User.objects.create(hero="Hero", description="Description", email="test@example.com")
        lst = List.objects.create(idUser=user, name="List Name", index=1, hidden=False)
        self.assertEqual(lst.name, "List Name")
        self.assertEqual(lst.index, 1)

    def test_unique_index_per_user(self):
        user = User.objects.create(hero="Hero", description="Description", email="test@example.com")
        List.objects.create(idUser=user, name="List 1", index=1, hidden=False)
        with self.assertRaises(ValidationError):
            lst = List(idUser=user, name="List 2", index=1)
            lst.full_clean()


class ListItemModelTest(TestCase):
    def test_create_list_item(self):
        user = User.objects.create(hero="Hero", description="Description", email="test@example.com")
        lst = List.objects.create(idUser=user, name="List Name", index=1, hidden=False)
        list_item = ListItem.objects.create(
            idList=lst,
            index=1,
            organisation="Org",
            name="Item Name",
            menuName="Menu Name",
            address="Address",
            period="Period",
            description="Description",
            hidden=False
        )
        self.assertEqual(list_item.name, "Item Name")
        self.assertEqual(list_item.index, 1)

    def test_unique_index_per_list(self):
        user = User.objects.create(hero="Hero", description="Description", email="test@example.com")
        lst = List.objects.create(idUser=user, name="List Name", index=1, hidden=False)
        ListItem.objects.create(idList=lst, index=1, organisation="Org", name="Item 1")
        with self.assertRaises(ValidationError):
            list_item = ListItem(idList=lst, index=1, organisation="Org", name="Item 2")
            list_item.full_clean()
