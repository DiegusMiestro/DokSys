FROM debian:8

# http://pythonclub.com.br/configurando-um-servidor-de-producao-para-aplicacoes-python.html
# http://docs.gunicorn.org/en/latest/deploy.html

MAINTAINER Diego Feitosa <diegusmiestro@gmail.com>

RUN apt update && apt-get install -y python3 python3-dev python3-pip virtualenv libpq-dev

RUN mkdir /app

WORKDIR /app

RUN virtualenv --python=python3 venv

RUN source venv/bin/activate

COPY ./config/requirements.pip ./
RUN pip install --no-cache-dir -r requirements.pip
