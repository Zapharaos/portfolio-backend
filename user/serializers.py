from rest_framework import serializers
from .models import Image, Technology, Project, Experience, Hero, About, Footer, User, Social


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
        fields = ['index', 'hidden', 'url', 'title', 'description', 'image', 'technologies']


class ExperienceSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Experience
        fields = ['index', 'hidden', 'title', 'organisation', 'period', 'location', 'url', 'urlShort',
                  'description', 'technologies']


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


class SocialSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Social
        fields = ['index', 'hidden', 'name', 'pseudo', 'url', 'image']


class UserSerializer(serializers.ModelSerializer):
    socials = SocialSerializer(many=True, source='social_set')
    hero = HeroSerializer()
    about = AboutSerializer()
    footer = FooterSerializer()
    projects = ProjectSerializer(many=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'location', 'locale', 'socials',
                  'hero', 'about', 'footer', 'projects']