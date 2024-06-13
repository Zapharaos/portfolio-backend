#!/bin/sh

echo "Waiting for the database to be ready..."
./wait-for-it.sh mysql:${MYSQL_PORT} --strict --timeout=30 -- echo "Database is up"

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start
exec "$@"
