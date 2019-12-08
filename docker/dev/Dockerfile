FROM python:3

LABEL MAINTAINER="Justin Ndwiga"
LABEL application="grind"
# Prevent dpkg errors
ENV TERM=xterm-256color
#Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
#python output set straight to terminal without buffering
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/projects/grind
WORKDIR /home/projects/grind
COPY ./requirements.txt /home/projects/grind/requirements.txt
RUN pip3 install --upgrade pip wheel
RUN pip3 install -r requirements.txt

# copy dev_entrypoint.sh
COPY bash/dev.sh /usr/local/bin/dev.sh
# copy project
COPY src /home/projects/grind
# run dev.sh
RUN chmod +x /usr/local/bin/dev.sh
ENTRYPOINT [ "dev.sh" ]
