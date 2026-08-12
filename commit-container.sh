#!/bin/sh

docker build -t microdom-cloud:latest .
docker tag microdom-cloud:latest ghcr.io/wpirri/microdom-cloud:latest
docker push ghcr.io/wpirri/microdom-cloud:latest

