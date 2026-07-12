# portfolio-backend

[![codecov](https://codecov.io/gh/Zapharaos/portfolio-backend/graph/badge.svg?token=6T49GCFCLY)](https://codecov.io/gh/Zapharaos/portfolio-backend)

Django + DRF backend powering my portfolio — [www.matthieu-freitag.com](https://www.matthieu-freitag.com/).
It exposes a small, public, read‑only API and everything is edited through the
Django admin.

## 📚 Documentation

Full documentation lives on **GitHub Pages**:
**<https://zapharaos.github.io/portfolio-backend/>**

- [Getting started](https://zapharaos.github.io/portfolio-backend/getting-started/)
- [API reference](https://zapharaos.github.io/portfolio-backend/api/)
- [Data model](https://zapharaos.github.io/portfolio-backend/models/) (every editable field)
- [Health checks](https://zapharaos.github.io/portfolio-backend/health-checks/)
- [Configuration](https://zapharaos.github.io/portfolio-backend/configuration/)
- [Deployment](https://zapharaos.github.io/portfolio-backend/deployment/)

The source is in [`docs/`](docs/) — preview locally with
`pip install -r docs/requirements.txt && mkdocs serve`.

## Quickstart

```bash
cp .env.dev .env                                  # configure (see Configuration docs)
docker compose -f docker-compose.dev.yml up       # http://localhost:8001/
docker exec -it portfolio-backend python manage.py createsuperuser
```

Then edit content at [http://localhost:8001/admin/](http://localhost:8001/admin/).

Not using Docker? `pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 8001`.

## Development

```bash
python manage.py test          # tests
coverage run manage.py test    # with coverage
flake8                         # lint
```

## Stack

Python 3.12 · Django 5.0 · Django REST Framework 3.15 · SQLite · Gunicorn · Nginx · Docker Compose.

## License

See [LICENSE](LICENSE).
