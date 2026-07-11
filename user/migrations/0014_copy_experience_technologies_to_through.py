from django.db import migrations


def forwards(apps, schema_editor):
    """Copy each row of the implicit Experience.technologies M2M table into the
    new ExperienceTechnology through model, assigning `position` by id order so
    the existing (arbitrary) order is preserved and stays stable."""
    Experience = apps.get_model('user', 'Experience')
    ExperienceTechnology = apps.get_model('user', 'ExperienceTechnology')

    Through = Experience.technologies.through
    for experience in Experience.objects.all():
        rows = (
            Through.objects
            .filter(experience_id=experience.id)
            .order_by('id')
            .values_list('technology_id', flat=True)
        )
        for position, technology_id in enumerate(rows):
            ExperienceTechnology.objects.get_or_create(
                experience_id=experience.id,
                technology_id=technology_id,
                defaults={'position': position},
            )


def backwards(apps, schema_editor):
    """Repopulate the implicit M2M table from ExperienceTechnology, then clear it."""
    Experience = apps.get_model('user', 'Experience')
    ExperienceTechnology = apps.get_model('user', 'ExperienceTechnology')

    Through = Experience.technologies.through
    for et in ExperienceTechnology.objects.all():
        Through.objects.get_or_create(
            experience_id=et.experience_id,
            technology_id=et.technology_id,
        )
    ExperienceTechnology.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_create_experience_technology'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
