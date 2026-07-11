from django.test import TestCase
from user.models import Project, Experience
from user.serializers import (
    SocialSerializer,
    UserSerializer, FileSerializer, TechnologySerializer, ProjectSerializer, ProjectLinkSerializer,
    ExperienceSerializer, FooterSerializer, ThemeSerializer,
    AboutSerializer, HeroSerializer, WorkSerializer, WorkItemSerializer,
)
from user.tests.utils import create_sample_user, create_sample_file, create_sample_technology, create_sample_project, \
    create_sample_project_technology, create_sample_project_link, create_sample_experience, \
    create_sample_experience_technology, create_sample_work_item, create_sample_work, create_sample_hero, \
    create_sample_about, create_sample_footer, create_sample_social, create_sample_theme


class FileSerializerTests(TestCase):

    def test_file_serializer_fields(self):
        serializer = FileSerializer(create_sample_file)
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'name', 'file',
            'creditsUrl', 'creditsShortUrl'
        })


class TechnologySerializerTests(TestCase):

    def test_technology_serializer_fields(self):
        serializer = TechnologySerializer(create_sample_technology)
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'name', 'color'
        })

    def test_technology_serializer_color_defaults_empty(self):
        serializer = TechnologySerializer(create_sample_technology())
        self.assertEqual(serializer.data['color'], '')


class ProjectSerializerTests(TestCase):

    def test_project_serializer_fields_and_nested_serializers(self):
        serializer = ProjectSerializer(create_sample_project())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'index', 'hidden', 'url', 'title',
            'description', 'image', 'technologies', 'links',
        })


    def test_project_technologies_ordered_by_position(self):
        project = Project.objects.create(
            index=1, hidden=False, url="https://project.com", title="Ordered",
            description="desc", image=create_sample_file()
        )
        tech_a = create_sample_technology(name="A")
        tech_b = create_sample_technology(name="B")
        tech_c = create_sample_technology(name="C")
        # Insert in a deliberately scrambled position order.
        create_sample_project_technology(project=project, technology=tech_b, position=20)
        create_sample_project_technology(project=project, technology=tech_a, position=10)
        create_sample_project_technology(project=project, technology=tech_c, position=30)

        data = ProjectSerializer(project).data
        self.assertEqual([t['name'] for t in data['technologies']], ['A', 'B', 'C'])


class ProjectLinkSerializerTests(TestCase):

    def test_project_link_serializer_fields(self):
        serializer = ProjectLinkSerializer(create_sample_project_link())
        self.assertEqual(set(serializer.fields.keys()), {
            'kind', 'url', 'label', 'icon', 'color', 'index',
        })

    def test_project_link_color_defaults_empty(self):
        serializer = ProjectLinkSerializer(create_sample_project_link())
        self.assertEqual(serializer.data['color'], '')

    def test_project_link_icon_defaults_null(self):
        serializer = ProjectLinkSerializer(create_sample_project_link())
        self.assertIsNone(serializer.data['icon'])

    def test_project_link_icon_serialized_when_set(self):
        link = create_sample_project_link(icon=create_sample_file(name="Icon"))
        data = ProjectLinkSerializer(link).data
        self.assertEqual(data['icon']['name'], 'Icon')

    def test_project_links_ordered_by_index(self):
        project = create_sample_project()
        create_sample_project_link(project=project, kind='github', index=20)
        create_sample_project_link(project=project, kind='website', index=10)
        create_sample_project_link(project=project, kind='docs', index=30)

        data = ProjectSerializer(project).data
        self.assertEqual([link['kind'] for link in data['links']], ['website', 'github', 'docs'])


class ExperienceSerializerTests(TestCase):

    def test_experience_serializer_fields_and_nested_serializer(self):
        serializer = ExperienceSerializer(create_sample_experience())
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'index', 'hidden', 'title', 'organisation',
            'period', 'location', 'url', 'urlShort',
            'description', 'technologies',
        })

    def test_experience_technologies_ordered_by_position(self):
        experience = Experience.objects.create(
            index=1, hidden=False, title="Ordered", organisation="Org",
            url="https://experience.com", description="desc",
        )
        tech_a = create_sample_technology(name="A")
        tech_b = create_sample_technology(name="B")
        tech_c = create_sample_technology(name="C")
        # Insert in a deliberately scrambled position order.
        create_sample_experience_technology(experience=experience, technology=tech_b, position=20)
        create_sample_experience_technology(experience=experience, technology=tech_a, position=10)
        create_sample_experience_technology(experience=experience, technology=tech_c, position=30)

        data = ExperienceSerializer(experience).data
        self.assertEqual([t['name'] for t in data['technologies']], ['A', 'B', 'C'])


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
            'index', 'hidden', 'name', 'pseudo', 'url', 'image', 'color',
        })
        self.assertIn('index', serializer.fields.keys())
        self.assertIn('hidden', serializer.fields.keys())
        self.assertIn('name', serializer.fields.keys())
        self.assertIn('pseudo', serializer.fields.keys())
        self.assertIn('url', serializer.fields.keys())
        self.assertIn('image', serializer.fields.keys())
        self.assertIn('color', serializer.fields.keys())

    def test_social_serializer_color_defaults_empty(self):
        serializer = SocialSerializer(create_sample_social())
        self.assertEqual(serializer.data['color'], '')


class ThemeSerializerTests(TestCase):

    def test_theme_serializer_fields(self):
        serializer = ThemeSerializer(create_sample_theme())
        self.assertEqual(set(serializer.fields.keys()), {
            'name', 'background', 'text', 'primary',
        })


class UserSerializerTests(TestCase):

    def test_user_serializer_fields_and_nested_serializers(self):
        serializer = UserSerializer(create_sample_user())  # Use instance for existing data
        # Check for presence of all expected fields
        self.assertEqual(set(serializer.fields.keys()), {
            'name', 'email', 'location', 'locale', 'timezone', 'logo', 'resume',
            'socials', 'theme', 'hero', 'about', 'work', 'footer',
        })

    def test_user_serializer_theme_null_when_absent(self):
        serializer = UserSerializer(create_sample_user())
        self.assertIsNone(serializer.data['theme'])

    def test_user_serializer_theme_nested_when_present(self):
        user = create_sample_user(theme=create_sample_theme(name="Ocean", primary="#00add8"))
        data = UserSerializer(user).data
        self.assertEqual(data['theme'], {
            'name': 'Ocean', 'background': '#181818', 'text': '#ffffff', 'primary': '#00add8',
        })
