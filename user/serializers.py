from rest_framework import serializers
from .models import User, Social, List, ListItem, Theme, Footer, SVG


class SVGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SVG
        fields = ['name', 'file']


class SocialSerializer(serializers.ModelSerializer):
    svg = SVGSerializer()

    class Meta:
        model = Social
        fields = ['index', 'name', 'pseudo', 'url', 'svg', 'hidden']


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


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ['title', 'subTitle', 'showLocation', 'showSocials', 'showEmail', 'showResume']


class UserSerializer(serializers.ModelSerializer):
    footer = FooterSerializer()

    socials = SocialSerializer(many=True, source='social_set')
    lists = ListSerializer(many=True, source='list_set')
    theme_light = ThemeSerializer()
    theme_dark = ThemeSerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'location', 'locale', 'footer',
                  'hero', 'description', 'logo', 'photo', 'curriculum',
                  'socials', 'lists', 'theme_light', 'theme_dark']
