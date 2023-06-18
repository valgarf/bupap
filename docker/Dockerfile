FROM python:3.11.4-slim-bookworm AS base

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1


########################
##### poetry image #####
########################

FROM base AS poetry-base
ENV PATH=$PATH:/root/.local/bin
# poetry in its own venv to not interfere with the app package.
# NOTE: script should adhere to the POETRY_VERSION environment variable
ADD https://install.python-poetry.org /poetry_installer.py
RUN python3 /poetry_installer.py \
    && poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
WORKDIR /app

# only copy necessary poetry stuff & install requirements
COPY poetry.lock pyproject.toml poetry.toml  /app/
RUN poetry install --without dev --no-root --no-interaction --no-ansi

#################################################################
##### debug image, app is copied as is & mounted at runtime #####
#################################################################

FROM poetry-base as debug

# install dev requirements
RUN poetry install --only dev --no-root --no-interaction --no-ansi

# Copy whole project & install in editable mode. Folder "./src" will be mounted from the outside when
# starting the container to allow quick restarts
COPY README.md LICENSE /app/
COPY ./src /app/src
RUN poetry install --no-interaction --only-root --no-ansi 

# copy config files to docker & prepare a runnable container
# NOTE: commands below are duplicated in debug & release containers and should always be the same
EXPOSE 80
COPY docker/target/* /
RUN mkdir ./data

# startup command
CMD "bupap"

############################################################
##### release build image, app is installed from wheel #####
############################################################

FROM poetry-base as release-build

# install current wheel
ARG APP_VERSION
COPY "./dist/bupap-${APP_VERSION}-py3-none-any.whl" /app/dist/
RUN python -m pip install --no-deps /app/dist/bupap-${APP_VERSION}-py3-none-any.whl 

######################################################################################
##### release image, only copy necessary stuff (no poetry) -> minimal image size #####
######################################################################################

FROM base as release
# all installed packages from build image
COPY --from=release-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=release-build /usr/local/bin/bupap* /usr/local/bin

# copy config files to docker & prepare a runnable container
# NOTE: commands below are duplicated in debug & release-test containers and should always be the same
EXPOSE 80
COPY docker/target/* /
RUN mkdir ./data

# startup command
CMD "bupap"

# ######################################################################################
# ##### release test image, extra test packages #####
# ######################################################################################

# FROM poetry-base as release-test

# # install test requirements
# RUN poetry install --without dev -E test --no-root --no-interaction --no-ansi

# # install current wheel
# ARG APP_VERSION
# COPY "./dist/bupap-${APP_VERSION}-py3-none-any.whl" /app/dist/
# RUN python -m pip install --no-deps /app/dist/bupap-${APP_VERSION}-py3-none-any.whl

# # copy config files to docker & prepare a runnable container
# # NOTE: commands below are duplicated in the debug & release containers and should always be the same
# EXPOSE 80
# COPY docker/target/* /
# RUN mkdir ./data

# # startup command
# CMD "pytest"
