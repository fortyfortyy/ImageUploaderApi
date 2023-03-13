FROM python:3.9.16-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN apk update && apk add python3-dev gcc libc-dev musl-dev libffi-dev openssl-dev

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./docker/local /app/docker

COPY . .