FROM ubuntu:latest
#FROM alpine:latest
#FROM python:3.8-slim

MAINTAINER Wale Adekoya "wale.adekoya@btinternet.com"

# install system dependencies
RUN apt-get update -y && apt-get install -y python3-pip python-dev

# copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# set work directory
WORKDIR /app

# install project dependencies
RUN pip install -r requirements.txt

# copy project
COPY . /app

EXPOSE 8041

#ENTRYPOINT ["python"]

 CMD ["waitress-serve", "--call", "--port=8041", "app:create_app"]
#CMD ["run.py"]


