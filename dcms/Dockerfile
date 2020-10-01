FROM python:3-alpine

RUN mkdir -p /opt/dcms
WORKDIR /opt/dcms

RUN apk add gcc make libffi-dev musl-dev postgresql-dev
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

COPY . /opt/dcms/

EXPOSE 80
ENTRYPOINT [ "./docker-entrypoint.sh" ]
