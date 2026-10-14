#!/bin/sh

echo "==== Arbol WEB ===="
rm -rf microdom_cloud_web
git clone https://github.com/wpirri/microdom_cloud_web.git
cd microdom_cloud_web
./deploy.sh
