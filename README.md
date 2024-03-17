# portfolio-backend

Repository related the backend of my own portfolio.

Link : www.matthieu-freitag.com/

## Setup

Copy the .env.example file into a new .env file and update the variables you want to change.

## Create django superuser

`docker exec -it django python manage.py createsuperuser`

## Dumb database

`docker exec mysql mysqldump -uMYSQL_ROOT_USER -pMYSQL_ROOT_PASSWORD MYSQL_DATABASE > dump.sql`

## Restore database

1. `docker exec -i mysql mysql -uMYSQL_ROOT_USER -pMYSQL_ROOT_PASSWORD -e "DROP DATABASE MYSQL_DATABASE";`
2. `docker exec -i mysql mysql -uMYSQL_ROOT_USER -pMYSQL_ROOT_PASSWORD -e "CREATE DATABASE MYSQL_DATABASE";`
3. `docker exec -i mysql mysql -uMYSQL_ROOT_USER -pMYSQL_ROOT_PASSWORD --database=MYSQL_DATABASE < dump.sql`