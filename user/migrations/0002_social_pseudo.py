# Generated by Django 5.0.3 on 2024-07-04 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='pseudo',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]