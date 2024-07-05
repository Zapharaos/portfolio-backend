from rest_framework import serializers
from .models import User, Social, Experience, Theme, Hero, About, Footer, Image, Technology, Project


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'file']


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['name']


class ProjectSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'index', 'description', 'image', 'url', 'technologies', 'hidden']


class SocialSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Social
        fields = ['index', 'name', 'pseudo', 'url', 'image', 'hidden']


class ExperienceSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Experience
        fields = ['title', 'organisation', 'period', 'location', 'url', 'urlShort',
                  'description', 'technologies', 'index', 'hidden']


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['name', 'todo']


class HeroSerializer(serializers.ModelSerializer):
    backgroundImage = ImageSerializer()

    class Meta:
        model = Hero
        fields = ['title', 'tagline', 'callToActionContent', 'backgroundImage']


class AboutSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    imageResponsive = ImageSerializer()

    class Meta:
        model = About
        fields = ['image', 'imageResponsive', 'description']


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ['title', 'subTitle', 'showLocation', 'showSocials', 'showEmail', 'showResume']


class UserSerializer(serializers.ModelSerializer):
    hero = HeroSerializer()
    about = AboutSerializer()
    footer = FooterSerializer()
    projects = ProjectSerializer(many=True)
    socials = SocialSerializer(many=True, source='social_set')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'location', 'locale',
                  'hero', 'about', 'footer', 'projects',
                  'socials', 'lists']
