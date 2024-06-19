# Generated by Django 5.0.3 on 2024-06-19 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_list_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listitem',
            name='index',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='social',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='social',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]