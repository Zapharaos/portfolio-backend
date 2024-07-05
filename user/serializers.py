from rest_framework import serializers
from .models import User, Social, List, ListItem, Theme, Hero, About, Footer, Image, Technology, Project


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
        fields = ['title', 'index', 'description', 'image', 'url', 'technologies']


class SocialSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Social
        fields = ['index', 'name', 'pseudo', 'url', 'image', 'hidden']


class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ['index', 'organisation', 'name', 'menuName', 'address', 'period', 'description', 'hidden']


class ListSerializer(serializers.ModelSerializer):
    items = ListItemSerializer(many=True, source='listitem_set')

    class Meta:
        model = List
        fields = ['name', 'index', 'hidden', 'items']


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
    lists = ListSerializer(many=True, source='list_set')

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'location', 'locale',
                  'hero', 'about', 'footer', 'projects',
                  'socials', 'lists']
