from django.db import migrations


def forwards(apps, schema_editor):
    """Copy each row of the implicit Project.technologies M2M table into the
    new ProjectTechnology through model, assigning `position` by id order so
    the existing (arbitrary) order is preserved and stays stable."""
    Project = apps.get_model('user', 'Project')
    ProjectTechnology = apps.get_model('user', 'ProjectTechnology')

    Through = Project.technologies.through
    for project in Project.objects.all():
        rows = (
            Through.objects
            .filter(project_id=project.id)
            .order_by('id')
            .values_list('technology_id', flat=True)
        )
        for position, technology_id in enumerate(rows):
            ProjectTechnology.objects.get_or_create(
                project_id=project.id,
                technology_id=technology_id,
                defaults={'position': position},
            )


def backwards(apps, schema_editor):
    """Repopulate the implicit M2M table from ProjectTechnology, then clear it."""
    Project = apps.get_model('user', 'Project')
    ProjectTechnology = apps.get_model('user', 'ProjectTechnology')

    Through = Project.technologies.through
    for pt in ProjectTechnology.objects.all():
        Through.objects.get_or_create(
            project_id=pt.project_id,
            technology_id=pt.technology_id,
        )
    ProjectTechnology.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_create_project_technology'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
