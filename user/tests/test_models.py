from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import (
    File, Technology, Project, Experience, WorkItem, Work, Hero, About, Footer, User, Social
)
from user.tests.utils import create_sample_user


class FileModelTest(TestCase):
    def test_create_file(self):
        file = File.objects.create(name="Test File", file="path/to/file.txt")
        self.assertEqual(file.name, "Test File")


class TechnologyModelTest(TestCase):
    def test_create_technology(self):
        technology = Technology.objects.create(name="Python")
        self.assertEqual(technology.name, "Python")


class ProjectModelTest(TestCase):
    def test_create_project(self):
        file = File.objects.create(name="Project Image", file="path/to/image.jpg")
        technology = Technology.objects.create(name="Django")
        project = Project.objects.create(
            index=1,
            hidden=False,
            url="https://project.com",
            title="Project Title",
            description="Project Description",
            image=file,
        )
        project.technologies.set([technology])
        self.assertEqual(project.title, "Project Title")
        self.assertEqual(project.technologies.count(), 1)


class ExperienceModelTest(TestCase):
    def test_create_experience(self):
        experience = Experience.objects.create(
            index=1,
            hidden=False,
            title="Experience Title",
            organisation="Some Organization",
            period="2020-2022",
            description="Experience Description",
        )
        self.assertEqual(experience.title, "Experience Title")

    def test_url_short_validation(self):
        with self.assertRaises(ValidationError):
            experience = Experience(
                urlShort="https://short.com",
            )
            experience.clean()

    def test_valid_url_short(self):
        experience = Experience.objects.create(
            index=1,
            hidden=False,
            title="Experience Title",
            organisation="Some Organization",
            period="2020-2022",
            description="Experience Description",
            url="https://experience.com",
            urlShort="https://short.com",
        )
        self.assertEqual(experience.urlShort, "https://short.com")


class WorkItemModelTest(TestCase):
    def test_create_work_item(self):
        file = File.objects.create(name="Project Image", file="path/to/image.jpg")
        project = Project.objects.create(
            index=1,
            hidden=False,
            url="https://project.com",
            title="Project Title",
            description="Project Description",
            image=file,
        )
        experience = Experience.objects.create(
            index=1,
            hidden=False,
            title="Experience Title",
            organisation="Some Organization",
            period="2020-2022",
            description="Experience Description",
        )
        work_item = WorkItem.objects.create(
            index=1,
            hidden=False,
            title="Work Item Title",
            showProjects=True,
        )
        work_item.projects.set([project])
        work_item.experiences.set([experience])
        self.assertEqual(work_item.title, "Work Item Title")
        self.assertEqual(work_item.projects.count(), 1)
        self.assertEqual(work_item.experiences.count(), 1)
        self.assertTrue(work_item.showProjects)
        self.assertFalse(work_item.showExperiences)

    def test_validation_show_fields(self):
        with self.assertRaises(ValidationError):
            work_item = WorkItem(
                index=1,
                hidden=False,
                title="Work Item Title",
                showProjects=True,
                showExperiences=True,
            )
            work_item.clean()


class WorkModelTest(TestCase):

    def test_create_work(self):
        work = Work.objects.create(content_type="work")
        self.assertEqual(work.content_type, "work")


class HeroModelTest(TestCase):
    def test_create_hero(self):
        file = File.objects.create(name="Background Image", file="path/to/image.jpg")
        hero = Hero.objects.create(
            title="Hero Title",
            tagline="Hero Tagline",
            callToActionContent="Call to Action Text",
            backgroundImage=file,
        )
        self.assertEqual(hero.title, "Hero Title")


class AboutModelTest(TestCase):
    def test_create_about(self):
        file = File.objects.create(name="About Image", file="path/to/image.jpg")
        about = About.objects.create(
            description="About Description",
            image=file,
        )
        self.assertEqual(about.description, "About Description")


class FooterModelTest(TestCase):
    def test_create_footer(self):
        footer = Footer.objects.create(
            title="Footer Title",
            subTitle="Footer Subtitle",
        )
        self.assertEqual(footer.title, "Footer Title")


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
        user = create_sample_user()
        file = File.objects.create(name="Social Icon", file="path/to/icon.jpg")
        social = Social.objects.create(
            idUser=user,
            index=1,
            name="Social Network",
            url="https://social.com",
            image=file,
        )
        self.assertEqual(social.name, "Social Network")
