# Swap Experience.technologies from the implicit M2M to the explicit
# ExperienceTechnology through model. State-only AlterField (the through table
# already exists from 0013 and is populated by 0014); the database side only
# drops the now-orphaned implicit M2M table.

from django.db import migrations, models

DROP_IMPLICIT_TABLE = 'DROP TABLE IF EXISTS "user_experience_technologies";'

RECREATE_IMPLICIT_TABLE = '''
CREATE TABLE IF NOT EXISTS "user_experience_technologies" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "experience_id" integer NOT NULL REFERENCES "user_experience" ("id") DEFERRABLE INITIALLY DEFERRED,
    "technology_id" integer NOT NULL REFERENCES "user_technology" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX IF NOT EXISTS "user_experience_technologies_experience_id_technology_id_uniq"
    ON "user_experience_technologies" ("experience_id", "technology_id");
'''


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_copy_experience_technologies_to_through'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='experience',
                    name='technologies',
                    field=models.ManyToManyField(
                        blank=True, through='user.ExperienceTechnology', to='user.technology'
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
