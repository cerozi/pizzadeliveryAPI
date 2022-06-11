FROM python:3.10.5-alpine3.15

ENV PYTHONUNBUFFERED = 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt


COPY . .
WORKDIR src/