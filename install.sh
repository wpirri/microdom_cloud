#!/bin/sh

#sudo mkdir -p /var/log/microdom
#sudo chmod 0777 /var/log/microdom
#sudo cp -uva etc/microdom.conf /etc

echo "Building microdom-cloud docker image..."
docker build -t microdom-cloud .
echo "Stop microdom-cloud..."
docker stop microdom-cloud
sleep 3
echo "Remove microdom-cloud..."
docker rm microdom-cloud
sleep 3
docker run -it \
  -d --restart unless-stopped \
  -e DBUSER=dompi_cloud \
  -e DBPASSWORD=dompi_cloud \
  -e DBHOST=192.168.10.32 \
  -e DBNAME=DB_DOMPICLOUD \
  --name microdom-cloud \
  -v /etc/microdom.conf:/app/etc/microdom.conf \
  -v /var/log/microdom:/app/logs \
  -v /var/lib/microdom_cloud/html:/app/html \
  -v /var/lib/microdom_cloud/download:/app/download \
  -p 8082:8082 microdom-cloud
