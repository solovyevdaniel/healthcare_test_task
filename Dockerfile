FROM python:3.11-slim

WORKDIR /opt/app

RUN apt-get update && \
    apt-get install -y gcc curl && \
    rm -rf /tmp/* && \
    rm -rf /var/lib/apt/lists/*

COPY . /opt/app
RUN pip install --no-cache-dir -r requirements.txt