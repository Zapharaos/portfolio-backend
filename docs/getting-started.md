# Getting started

## Requirements

- [Docker](https://www.docker.com/) and Docker Compose, **or** Python 3.12 with a
  virtual environment.

## Environment

Copy the example env file and adjust the values:

```bash
cp .env.dev .env          # local development
# or, for production:
cp .env.prod.example .env
```

The full list of variables is in [Configuration](configuration.md).

## Run with Docker (recommended)

```bash
docker compose -f docker-compose.dev.yml up      # development
docker compose -f docker-compose.prod.yml up -d  # production
```

The API is then served on `http://localhost:8001/` (dev).

!!! note "Entrypoint error"
    If you hit `exec /usr/src/app/entrypoint.sh: no such file or directory`,
    replace `#!/bin/sh` with `#!/bin/bash` at the top of `entrypoint.sh`
    (line‑ending issue on some hosts).

## Run without Docker

```bash
python -m venv .venv && . .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

## Create an admin user

```bash
# Docker
docker exec -it portfolio-backend python manage.py createsuperuser
# Local
python manage.py createsuperuser
```

Then open the admin and start editing content:

- Dev: [http://localhost:8001/admin/](http://localhost:8001/admin/)
- Prod: `https://api.yourdomain.com/admin/`

The site is driven by a **single `User` instance** (a singleton — creating a
second one raises an error). Fill it in first, then add projects, experiences,
socials, etc. See the [Data model](models.md).

## Tests & linting

```bash
python manage.py test          # unit tests
coverage run manage.py test    # with coverage
flake8                         # style (migrations excluded, max line 119)
```

## Preview the docs locally

```bash
pip install -r docs/requirements.txt
mkdocs serve      # http://127.0.0.1:8000
```
