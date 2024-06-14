# Pull base image
FROM python:latest

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

# Run the command to start the Django development server
RUN chmod +x /usr/src/app/wait-for-it.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]