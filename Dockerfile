# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /prueba
COPY . /prueba/
RUN pip install pipenv
RUN pipenv install
