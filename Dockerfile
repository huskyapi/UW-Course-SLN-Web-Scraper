FROM python:3.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    # Prevent Python from creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    ## pip ##
    PIP_DISABLE_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    ## poetry ##
    POETRY_VERSION=1.0.10 \
    # Make Poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # Make Poetry create virtual environment in project root
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # No interaction questions from Poetry
    POETRY_NO_INTERACTION=1 \
    ## paths ##
    # Location of requirements + virtual environment
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv/"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # dependencies for installing poetry
    curl \
    # dependencies for building python dependencies
    build-essential

# Install poetry (using $POETRY_VERSION and $POETRY_HOME)
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Copy over project requirement files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Install runtime dependencies (using $POETRY_VIRTUALENVS_IN_PROJECT)
RUN poetry install --no-dev

# Development image for development and testing
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install
RUN poetry shell

COPY ./scraper $PYSETUP_PATH/scraper
COPY main.py $PYSETUP_PATH/

