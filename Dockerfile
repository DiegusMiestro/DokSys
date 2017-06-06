# Apache2 Server
FROM httpd:2
RUN apt-get install libapache2-mod-wsgi-py3

# Python Software Language
FROM python:3
RUN mkdir /app
WORKDIR /app
EXPOSE 8000
COPY ./python/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN django-admin startproject doksys .
CMD [ "python", "manage.py", "runserver"]

# Postgres Database
FROM postgres:9
