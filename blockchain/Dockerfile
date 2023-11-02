# pull official base image
FROM bitnami/python:3.11.5

ARG NODE_HOME=/usr/src/node

# set working directory
WORKDIR ${NODE_HOME}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# install system dependencies
RUN apt-get update \
  && apt-get clean

# install python dependencies
COPY requirements ${NODE_HOME}/requirements

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/dev.txt

# copy project
COPY . ${NODE_HOME}

RUN chmod +x entrypoint.sh