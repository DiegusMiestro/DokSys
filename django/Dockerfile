FROM debian:8
MAINTAINER Diego Feitosa <diegusmiestro@gmail.com>
RUN apt-get update && apt-get install -y python3 python3-dev python3-pip libpq-dev && mkdir /app
WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
RUN django-admin startproject main .
EXPOSE 8000
CMD ["python3", "manage.py", "runserver"]
