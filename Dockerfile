# Pull base image
# Pinned to 3.12: Django 5.0.x does not support Python 3.13/3.14
FROM python:3.12

# Set working directory
WORKDIR /usr/src/app
COPY . /usr/src/app/

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]