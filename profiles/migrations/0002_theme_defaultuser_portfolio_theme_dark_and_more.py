# Generated by Django 5.0.3 on 2024-06-14 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('background', models.CharField(max_length=7)),
                ('color', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='default_user', to='profiles.user')),
            ],
        ),
        migrations.AddField(
            model_name='portfolio',
            name='theme_dark',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dark_theme_portfolios', to='profiles.theme'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='theme_light',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='light_theme_portfolios', to='profiles.theme'),
        ),
    ]
