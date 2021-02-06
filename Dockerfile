FROM python:3.9-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 bcrypt \
    && apk del build-deps

RUN apk --update add postgresql-client

RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./entrypoint.sh ./entrypoint.sh
COPY . .

ENTRYPOINT ["./entrypoint.sh"]
