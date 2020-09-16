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
    ## Web Driver ##
    CHROME_DRIVER_VERSION="LATEST_RELEASE" \
    ## paths ##
    # Location of requirements + virtual environment
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv/"\
    WEBDRIVER_CHROME_PATH="/opt/webdriver/chrome"


ENV PATH="$WEBDRIVER_CHROME_PATH:$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # dependencies for installing poetry
    curl \
    # dependencies for building python dependencies
    build-essential \
    # dependencies for web driver
    wget \
    gnupg

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Get Web Driver (Chrome) 
RUN mkdir -p $WEBDRIVER_CHROME_PATH
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d $WEBDRIVER_CHROME_PATH
ENV DISPLAY=:99

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