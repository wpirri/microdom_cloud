#!/bin/sh

echo "==== Servicio microdom ===="
echo "Stop..."
docker stop microdom-cloud
sleep 1
echo "Remove..."
docker rm microdom-cloud
sleep 1
echo "Update & Start..."
docker pull ghcr.io/wpirri/microdom-cloud:latest

docker run -it -d --restart unless-stopped \
  -e DBUSER=dompi_web \
  -e DBPASSWORD=dompi_web \
  -e DBHOST=172.17.0.1 \
  -e DBNAME=DB_DOMPICLOUD \
  --name microdom-cloud \
  -v /etc/microdom.conf:/app/etc/microdom.conf \
  -v /var/log/microdom:/app/logs \
  -v /var/lib/microdom_cloud/html:/app/html \
  -v /var/lib/microdom_cloud/download:/app/download \
  -p 8082:8082 \
  ghcr.io/wpirri/microdom-cloud:latest

