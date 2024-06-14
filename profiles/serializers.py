from rest_framework import serializers
from .models import User, Portfolio, Social, List, ListItem, DefaultUser, Theme


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['name', 'url', 'hidden']


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
        fields = ['name', 'background', 'color']


class UserSerializer(serializers.ModelSerializer):
    socials = SocialSerializer(many=True, source='social_set')
    lists = ListSerializer(many=True, source='list_set')

    class Meta:
        model = User
        fields = ['id', 'hero', 'logo', 'description', 'photo', 'curriculum', 'socials', 'lists']


class PortfolioSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='idUser')
    theme_light = ThemeSerializer()
    theme_dark = ThemeSerializer()

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'theme_light', 'theme_dark']
