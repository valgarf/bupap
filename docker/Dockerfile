FROM python:3.11.4-slim-bookworm AS python-base

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1

# System deps:
RUN pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
COPY docker/target/* /
WORKDIR /app


############################################
##### debug image, app is copied as is #####
############################################

FROM python-base as debug

# Copy whole project (maybe )
COPY ./src /app/src
COPY poetry.lock pyproject.toml poetry.toml README.md LICENSE /app/
# editable install
RUN poetry install --no-interaction --no-ansi \
    && mkdir ./data

CMD "bupap"

######################################################
##### release image, app is installed from wheel #####
######################################################

FROM python-base as release

COPY poetry.lock pyproject.toml poetry.toml /app/
ARG APP_VERSION
COPY "./dist/bupap-${APP_VERSION}-py3-none-any.whl" /app/dist/

RUN poetry install --no-root --no-dev --no-interaction --no-ansi \
    && python -m pip install /app/dist/bupap-${APP_VERSION}-py3-none-any.whl \
    && mkdir ./data

CMD "bupap"



