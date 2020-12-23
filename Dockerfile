FROM python:3.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    # Prevent Python from creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    ## pip ##
    PIP_DISABLE_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    ## paths ##
    # Location of requirements + virtual environment
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv/"

ENV PATH="$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # dependencies for installing poetry
    curl \
    # dependencies for building python dependencies
    build-essential


# Copy over project requirement files
WORKDIR $PYSETUP_PATH
COPY requirements.txt ./


# Development image for development and testing
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built venv
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Install runtime dependencies
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./scraper $PYSETUP_PATH/scraper
COPY main.py $PYSETUP_PATH/

