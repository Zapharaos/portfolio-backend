# Generated by Django 5.0.3 on 2024-07-05 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workitem',
            name='showExperiences',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workitem',
            name='showProjects',
            field=models.BooleanField(default=False),
        ),
    ]
