from rest_framework import serializers
from .models import User, Social, List, ListItem, Theme, About, Footer, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'file']


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
    about = AboutSerializer()
    footer = FooterSerializer()

    socials = SocialSerializer(many=True, source='social_set')
    lists = ListSerializer(many=True, source='list_set')
    theme_light = ThemeSerializer()
    theme_dark = ThemeSerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'location', 'locale', 'about', 'footer',
                  'hero', 'description', 'logo', 'photo', 'curriculum',
                  'socials', 'lists', 'theme_light', 'theme_dark']
