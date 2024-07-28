﻿FROM python:3.10

ENV PYTHONUNBUFFERED 1 #python 애플리케이션의 출력 버퍼링을 비활성화하는 데 사용되는 환경 변수
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]