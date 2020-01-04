#we used a Docker multi-stage build to reduce the final image size. 
#Essentially, builder is a temporary image that's used for building the Python wheels.
#The wheels are then copied over to the final production image and the builder image is discarded.

###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.0-alpine as builder

LABEL MAINTAINER="Justin Ndwiga"
LABEL application="grind"

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies needed ot build wheels
# apk - alpine base system installs
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

# lint
RUN pip3 install --upgrade pip
RUN pip3 install flake8
COPY . /usr/src/app/
# RUN flake8 --ignore=E501,F401 .
# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.0-alpine

# create directory for the app user
RUN mkdir -p /home/projects

# create the app user to prevent user from running as root(default)
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/projects
ENV APP_HOME=/home/projects/grind
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq 
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./bash/prod.sh $APP_HOME

# copy project
COPY src $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

RUN chmod +x /home/projects/grind/prod.sh
# run entrypoint.prod.sh
ENTRYPOINT ["/home/projects/grind/prod.sh"]
