from django.test import TestCase
from user.serializers import (
    SocialSerializer,
    UserSerializer, FileSerializer, TechnologySerializer, ProjectSerializer, ExperienceSerializer, FooterSerializer,
    AboutSerializer, HeroSerializer, WorkSerializer, WorkItemSerializer,
)
from user.tests.utils import create_sample_user, create_sample_file, create_sample_technology, create_sample_project, \
    create_sample_experience, create_sample_work_item, create_sample_work, create_sample_hero, create_sample_about, \
    create_sample_footer, create_sample_social


class FileSerializerTests(TestCase):

    def test_file_serializer_fields(self):
        serializer = FileSerializer(create_sample_file)
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'name', 'file'
        })


class TechnologySerializerTests(TestCase):

    def test_technology_serializer_fields(self):
        serializer = TechnologySerializer(create_sample_technology)
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'name'
        })


class ProjectSerializerTests(TestCase):

    def test_project_serializer_fields_and_nested_serializers(self):
        serializer = ProjectSerializer(create_sample_project())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'index', 'hidden', 'url', 'title',
            'description', 'image', 'technologies',
        })


class ExperienceSerializerTests(TestCase):

    def test_experience_serializer_fields_and_nested_serializer(self):
        serializer = ExperienceSerializer(create_sample_experience())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'index', 'hidden', 'title', 'organisation',
            'period', 'location', 'url', 'urlShort',
            'description', 'technologies',
        })


class WorkItemSerializerTests(TestCase):

    def test_experience_serializer_fields_and_nested_serializer(self):
        serializer = WorkItemSerializer(create_sample_work_item())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'index', 'hidden', 'title', 'projects', 'experiences',
            'showProjects', 'showExperiences',
        })


class WorkSerializerTests(TestCase):

    def test_experience_serializer_fields_and_nested_serializer(self):
        serializer = WorkSerializer(create_sample_work())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'items'
        })


class HeroSerializerTests(TestCase):

    def test_hero_serializer_fields(self):
        serializer = HeroSerializer(create_sample_hero())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'title', 'tagline', 'callToActionContent', 'backgroundImage',
        })


class AboutSerializerTests(TestCase):

    def test_about_serializer_fields(self):
        serializer = AboutSerializer(create_sample_about())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'image', 'imageResponsive', 'description',
        })


class FooterSerializerTests(TestCase):

    def test_footer_serializer_fields(self):
        serializer = FooterSerializer(create_sample_footer())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'title', 'subTitle', 'showLocation', 'showSocials', 'showEmail', 'showResume',
        })
        self.assertIn('title', serializer.fields.keys())
        self.assertIn('subTitle', serializer.fields.keys())
        self.assertIn('showLocation', serializer.fields.keys())
        self.assertIn('showSocials', serializer.fields.keys())
        self.assertIn('showEmail', serializer.fields.keys())
        self.assertIn('showResume', serializer.fields.keys())


class SocialSerializerTests(TestCase):

    def test_social_serializer_fields(self):
        serializer = SocialSerializer(create_sample_social())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'index', 'hidden', 'name', 'pseudo', 'url', 'image',
        })
        self.assertIn('index', serializer.fields.keys())
        self.assertIn('hidden', serializer.fields.keys())
        self.assertIn('name', serializer.fields.keys())
        self.assertIn('pseudo', serializer.fields.keys())
        self.assertIn('url', serializer.fields.keys())
        self.assertIn('image', serializer.fields.keys())


class UserSerializerTests(TestCase):

    def test_user_serializer_fields_and_nested_serializers(self):
        serializer = UserSerializer(create_sample_user())  # Use instance for existing data
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'name', 'email', 'location', 'locale', 'logo', 'resume',
            'socials', 'hero', 'about', 'work', 'footer',
        })
