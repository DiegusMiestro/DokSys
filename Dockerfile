FROM python:3
MAINTAINER Diego Feitosa <diegusmiestro@gmail.com>
WORKDIR /app
COPY ./app /app
RUN pip3 install -r requirements.txt
