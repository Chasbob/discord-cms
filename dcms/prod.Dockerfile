FROM python:3-alpine AS POETRY
ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /bin/get-poetry

ARG POETRY_HOME=/etc/poetry
ARG POETRY_VERSION=1.0.5
RUN python /bin/get-poetry

WORKDIR /poetry
COPY ./pyproject.toml ./poetry.lock ./
RUN /etc/poetry/bin/poetry export -f requirements.txt > requirements.txt

FROM python:3-alpine

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev

WORKDIR /opt/dcms

COPY --from=poetry /poetry/requirements.txt .

RUN pip install -r /opt/dcms/requirements.txt

RUN apk --purge del .build-deps

COPY . /opt/dcms

EXPOSE 80

ARG API_ROOT_PATH
ENV APP_MODULE=dcms:app
ENV API_ROOT_PATH=${API_ROOT_PATH}
