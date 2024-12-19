#!/bin/bash

# Generate static/
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start
exec "$@"
