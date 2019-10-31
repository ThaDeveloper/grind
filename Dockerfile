FROM python:3

LABEL MAINTAINER="Justin Ndwiga"
LABEL application="grind"
# Prevent dpkg errors
ENV TERM=xterm-256color

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip3 install --upgrade pip wheel
RUN pip3 install -r src/requirements.txt
