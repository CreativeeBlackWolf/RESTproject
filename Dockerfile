# pull official base image
FROM python:3.9.7-alpine

# set work directory
WORKDIR /bank

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade --no-cache-dir pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /bank