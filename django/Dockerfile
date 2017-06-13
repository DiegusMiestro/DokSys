FROM debian:8
MAINTAINER Diego Feitosa <diegusmiestro@gmail.com>
EXPOSE 80 8000
RUN apt-get update && apt-get install -y python3 python3-dev python3-pip libpq-dev && mkdir /app
WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
RUN django-admin startproject main .
