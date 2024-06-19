#!/bin/sh

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start
exec "$@"
