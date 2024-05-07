FROM python:3.12-slim

WORKDIR /appFROM python:3.12-slim

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app/* ./
