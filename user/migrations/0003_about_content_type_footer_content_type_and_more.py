# Generated by Django 5.0.3 on 2024-07-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_delete_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='content_type',
            field=models.CharField(default='about', max_length=255),
        ),
        migrations.AddField(
            model_name='footer',
            name='content_type',
            field=models.CharField(default='footer', max_length=255),
        ),
        migrations.AddField(
            model_name='hero',
            name='content_type',
            field=models.CharField(default='hero', max_length=255),
        ),
    ]