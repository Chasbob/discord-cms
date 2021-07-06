FROM python:3.8-slim as poetry

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PIP_NO_CACHE_DIR=off 
ENV PIP_DISABLE_PIP_VERSION_CHECK=on 
ENV PIP_DEFAULT_TIMEOUT=100 
ENV POETRY_HOME="/opt/poetry" 
ENV POETRY_VERSION=1.1.7
ENV POETRY_VIRTUALENVS_IN_PROJECT=true 
ENV POETRY_NO_INTERACTION=1 
ENV PYSETUP_PATH="/opt/pysetup" 
ENV VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ADD https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py /bin/install-poetry.py

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

RUN python /bin/install-poetry.py

FROM poetry AS base-builder
ARG DIR
RUN mkdir -p /app/${DIR}
WORKDIR /app

# RUN apk add gcc make libffi-dev musl-dev postgresql-dev

COPY ./orm ./orm
COPY ./$DIR/pyproject.toml ./$DIR/poetry.lock ./$DIR
WORKDIR /app/${DIR}

FROM base-builder AS builder

RUN poetry install --no-dev

COPY . /app

RUN apt install -y --no-install-recommends libpq-dev

ENTRYPOINT [ "./docker-entrypoint.sh" ]

# FROM base-builder AS prod
#
# RUN poetry export -f requirements.txt > requirements.txt
#
# COPY . /app

