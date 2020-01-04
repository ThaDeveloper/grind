FROM python:3

LABEL MAINTAINER="Justin Ndwiga"
LABEL application="grind"
# Prevent dpkg errors
ENV TERM=xterm-256color
#Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
#python output set straight to terminal without buffering
ENV PYTHONUNBUFFERED 1

WORKDIR /home/projects/grind
COPY ./requirements.txt /home/projects/grind/requirements.txt
RUN pip3 install --upgrade pip wheel
RUN pip3 install -r requirements.txt

# copy test_entrypoint.sh
COPY bash/test.sh /usr/local/bin/test.sh
# copy project
COPY . /home/projects/grind
# run test.sh
RUN chmod +x /usr/local/bin/test.sh
ENTRYPOINT [ "test.sh" ]
