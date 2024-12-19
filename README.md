# portfolio-backend

[![codecov](https://codecov.io/gh/Zapharaos/portfolio-backend/graph/badge.svg?token=6T49GCFCLY)](https://codecov.io/gh/Zapharaos/portfolio-backend)

Repository related the backend of my own portfolio.

Link : www.matthieu-freitag.com/

## Start the server

### Setup

Copy the `.env.dev` file into a new `.env` file and update the variables you want to change.<br>
If you are deploying for production, please copy `.env.prod.example` instead.

### Run the project

`docker-compose -f .\docker-compose.[environment].yml up`

Please replace `[environment]` by either `dev` or `prod`.

### Entrypoint error

```exec /usr/src/app/entrypoint.sh: no such file or directory```

You might run into the above error when starting the server.<br>
In that case, try replacing `#!/bin/sh` with `#!/bin/bash` inside `entrypoint.sh`.

### Create django superuser

`docker exec -it django python manage.py createsuperuser`

### Access the admin panel

Head to one of the below URL and login with the superuser you created.

- [http://localhost:8001/admin/](http://localhost:8001/admin/) for the development environment.
- [https://api.yourdomain.com.com/admin/](https://api.yourdomain.com/admin/) for the production environment.

## Customize your portfolio

Know that you've logged in, you can customize your portfolio by adding new projects, skills, etc.