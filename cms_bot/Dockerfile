FROM python:3-alpine

RUN mkdir -p /opt/cms_bot
WORKDIR /opt/cms_bot

RUN apk add gcc make libffi-dev musl-dev postgresql-dev
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

COPY . /opt/cms_bot/

ENTRYPOINT [ "./docker-entrypoint.sh" ]
