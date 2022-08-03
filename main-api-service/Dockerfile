FROM python:3.10.5-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev gcc

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
