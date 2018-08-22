#
# MongoDB Dockerfile
#
# https://github.com/dockerfile/mongodb
#

# Pull base image.
# FROM ubuntu:14.04
FROM python:3.5

RUN pip install requests flask pymongo
# Install MongoDB.
# RUN \
#   # apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 && \
#   # echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > /etc/apt/sources.list.d/mongodb.list && \
#   apt-get update && \
#   apt-get install -y vim && \
#   apt-get install -y python2.7 python-pip && \
#   sudo pip install pymongo && \ 
#   sudo pip install requests && \
#   sudo pip install flask
# apt-get install -y mongodb-org && \
# rm -rf /var/lib/apt/lists/*

# Define mountable directories.
# VOLUME ["/data/db"]

# Define working directory.
WORKDIR /usr/src/app
COPY cryptongo/agent/main.py ./agent.py
# WORKDIR /data
# ADD script-curso.js /data
# ADD cryptongo /data


# Define default command.
CMD [ "python", "agent.py" ]
# CMD ["mongod"]

# Expose ports.
#   - 27017: process
#   - 28017: http
# EXPOSE 27017
# EXPOSE 28017