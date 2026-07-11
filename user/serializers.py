from rest_framework import serializers
from .models import (
    File, Technology, Project, ProjectLink, Experience, WorkItem, Work, Hero, About, Footer, User, Social
)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['name', 'file', 'creditsUrl', 'creditsShortUrl']


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['name', 'color']


class ProjectLinkSerializer(serializers.ModelSerializer):
    icon = FileSerializer()

    class Meta:
        model = ProjectLink
        fields = ['kind', 'url', 'label', 'icon', 'color', 'index']


class ProjectSerializer(serializers.ModelSerializer):
    image = FileSerializer()
    technologies = serializers.SerializerMethodField()
    links = ProjectLinkSerializer(many=True)

    class Meta:
        model = Project
        fields = ['index', 'hidden', 'url', 'title', 'description', 'image', 'technologies', 'links']

    def get_technologies(self, obj):
        # The through model's Meta.ordering does not apply to M2M traversal,
        # so order explicitly by ProjectTechnology.position.
        techs = obj.technologies.order_by('projecttechnology__position')
        return TechnologySerializer(techs, many=True).data


class ExperienceSerializer(serializers.ModelSerializer):
    technologies = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = ['index', 'hidden', 'title', 'organisation', 'period', 'location', 'url', 'urlShort',
                  'description', 'technologies']

    def get_technologies(self, obj):
        # The through model's Meta.ordering does not apply to M2M traversal,
        # so order explicitly by ExperienceTechnology.position.
        techs = obj.technologies.order_by('experiencetechnology__position')
        return TechnologySerializer(techs, many=True).data


class WorkItemSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    experiences = ExperienceSerializer(many=True)

    class Meta:
        model = WorkItem
        fields = ['index', 'hidden', 'title', 'projects', 'experiences', 'showProjects', 'showExperiences']


class WorkSerializer(serializers.ModelSerializer):
    items = WorkItemSerializer(many=True)

    class Meta:
        model = Work
        fields = ['items']


class HeroSerializer(serializers.ModelSerializer):
    backgroundImage = FileSerializer()

    class Meta:
        model = Hero
        fields = ['title', 'tagline', 'callToActionContent', 'backgroundImage']


class AboutSerializer(serializers.ModelSerializer):
    image = FileSerializer()
    imageResponsive = FileSerializer()

    class Meta:
        model = About
        fields = ['image', 'imageResponsive', 'description']


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ['title', 'subTitle', 'showLocation', 'showSocials', 'showEmail', 'showResume']


class SocialSerializer(serializers.ModelSerializer):
    image = FileSerializer()

    class Meta:
        model = Social
        fields = ['index', 'hidden', 'name', 'pseudo', 'url', 'image', 'color']


class UserSerializer(serializers.ModelSerializer):
    logo = FileSerializer()
    resume = FileSerializer()
    socials = SocialSerializer(many=True, source='social_set')
    hero = HeroSerializer()
    about = AboutSerializer()
    work = WorkSerializer()
    footer = FooterSerializer()

    class Meta:
        model = User
        fields = ['name', 'email', 'location', 'locale', 'logo', 'resume', 'socials',
                  'hero', 'about', 'work', 'footer']
