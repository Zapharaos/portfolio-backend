from django.core.management.base import BaseCommand

from user.health import monitored_projects, refresh_project


class Command(BaseCommand):
    help = 'Vérifie les healthUrl des projets et met à jour leur état (run manuel/optionnel).'

    def handle(self, *args, **options):
        for project in monitored_projects():
            ok = refresh_project(project)
            self.stdout.write(
                f'{project.title}: {"up" if ok else "down"} '
                f'(healthUp={project.healthUp}, failures={project.healthFailures})'
            )
