# Use an official Python runtime as a parent image
FROM python:3.9

ARG USER_ID
ARG GROUP_ID

RUN test -n "${USER_ID}" || (echo '!!!!!: Please set USER_ID environment variable to $(id -u)' && false)
RUN test -n "${GROUP_ID}" || (echo '!!!!!: Please set GROUP_ID environment variable to $(id -g)' && false)

# Set environment variables for Poetry to avoid virtual environment creation inside the container
ENV PYTHONUNBUFFERED=1 \
    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ROOT_PATH=/home/dev/app \
    APP_DATA_PATH=/home/dev/data \
    # https://python-poetry.org/docs/configuration/#virtualenvsin-project
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.4.1 \
    POETRY_EXPERIMENTAL_NEW_INSTALLER=false \
    UNAME=dev \
    GNAME=dev

# Set the working directory in the container
WORKDIR /home/dev/app

# Install system dependencies needed for Poetry and Python build tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

CMD ["bash"]