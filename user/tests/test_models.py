from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User
from user.tests.utils import create_sample_user, create_sample_file, create_sample_technology, create_sample_project, \
    create_sample_experience, create_sample_work_item, create_sample_work, create_sample_hero, create_sample_about, \
    create_sample_footer, create_sample_social


class FileModelTest(TestCase):
    def test_create_file(self):
        file = create_sample_file(name="Name")
        self.assertEqual(file.name, "Name")

    def test_url_short_validation(self):
        with self.assertRaises(ValidationError):
            file = create_sample_file(name="Name", creditsUrl=None)
            file.clean()


class TechnologyModelTest(TestCase):
    def test_create_technology(self):
        technology = create_sample_technology(name="Name")
        self.assertEqual(technology.name, "Name")


class ProjectModelTest(TestCase):
    def test_create_project(self):
        project = create_sample_project(title="Title")
        self.assertEqual(project.title, "Title")


class ExperienceModelTest(TestCase):
    def test_create_experience(self):
        experience = create_sample_experience(title="Title")
        self.assertEqual(experience.title, "Title")

    def test_url_short_validation(self):
        with self.assertRaises(ValidationError):
            experience = create_sample_experience(title="Title", url=None)
            experience.clean()


class WorkItemModelTest(TestCase):
    def test_create_work_item(self):
        work_item = create_sample_work_item(title="Title")
        self.assertEqual(work_item.title, "Title")

    def test_validation_show_fields(self):
        with self.assertRaises(ValidationError):
            work_item = create_sample_work_item(title="Title", showProjects=True, showExperiences=True)
            work_item.clean()


class WorkModelTest(TestCase):

    def test_create_work(self):
        work = create_sample_work(content_type="Work")
        self.assertEqual(work.content_type, "Work")


class HeroModelTest(TestCase):
    def test_create_hero(self):
        hero = create_sample_hero(content_type="Hero")
        self.assertEqual(hero.content_type, "Hero")


class AboutModelTest(TestCase):
    def test_create_about(self):
        about = create_sample_about(content_type="About")
        self.assertEqual(about.content_type, "About")


class FooterModelTest(TestCase):
    def test_create_footer(self):
        footer = create_sample_footer(content_type="Footer")
        self.assertEqual(footer.content_type, "Footer")


class UserModelTest(TestCase):

    def test_unique_user(self):
        create_sample_user()
        with self.assertRaises(ValidationError):
            create_sample_user()

    def test_user_creation(self):
        create_sample_user()
        self.assertEqual(User.objects.count(), 1)


class SocialModelTest(TestCase):
    def test_create_social(self):
        social = create_sample_social(name="Name")
        self.assertEqual(social.name, "Name")
