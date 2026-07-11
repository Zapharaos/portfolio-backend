# Swap Project.technologies from the implicit M2M to the explicit
# ProjectTechnology through model. State-only AlterField (the through table
# already exists from 0007 and is populated by 0008); the database side only
# drops the now-orphaned implicit M2M table.

from django.db import migrations, models

DROP_IMPLICIT_TABLE = 'DROP TABLE IF EXISTS "user_project_technologies";'

RECREATE_IMPLICIT_TABLE = '''
CREATE TABLE IF NOT EXISTS "user_project_technologies" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "project_id" integer NOT NULL REFERENCES "user_project" ("id") DEFERRABLE INITIALLY DEFERRED,
    "technology_id" integer NOT NULL REFERENCES "user_technology" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX IF NOT EXISTS "user_project_technologies_project_id_technology_id_uniq"
    ON "user_project_technologies" ("project_id", "technology_id");
'''


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_copy_technologies_to_through'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='project',
                    name='technologies',
                    field=models.ManyToManyField(
                        blank=True, through='user.ProjectTechnology', to='user.technology'
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql=DROP_IMPLICIT_TABLE,
                    reverse_sql=RECREATE_IMPLICIT_TABLE,
                ),
            ],
        ),
    ]
