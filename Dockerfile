FROM python:3.11-slim

# Banned to create cache (.pyc)
ENV PYTHONDONTWRITEBYTECODE 1
# Banned to buffer logs
ENV PYTHONUNBUFFERED 1


# Update pip
RUN pip install --upgrade pip


# Make dir from our django project
RUN mkdir code
# Point work dir
WORKDIR /code


# Add requirements
ADD requirements.txt /code/
# Install requirements
RUN pip install -r requirements.txt


# Install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Add our project in workdir
ADD . /code/


# Run gunicorn
CMD [ "gunicorn", "store.wsgi:application", "-b", "0.0.0.0:8000" ]


