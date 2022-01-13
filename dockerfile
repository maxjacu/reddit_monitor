FROM python:3.7-slim
MAINTAINER Max Jacubowsky <maxjacu@gmail.com>
ENV RATELIMIT_SECONDS=30
ENV SUBREDDIT_NAME=mangaswap

ARG DEBIAN_FRONTEND=noninteractive

COPY . /app/

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -e .

WORKDIR /app/src

ENTRYPOINT [ "python3", "main.py" ]
