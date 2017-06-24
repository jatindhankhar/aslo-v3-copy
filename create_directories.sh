#!/bin/sh

current_user=$USER
echo "Creating directories ....."

echo "Creating directory for storing downloaded repositories"
mkdir -p /tmp/activities
#chmod +w -R /tmp/activities
sudo setfacl -m u:$current_user:rwx /var/tmp/activities

echo "Creating directory to store downloded bundled activities"

sudo mkdir -p /opt/bundles
#sudo chmod +w -R /opt/bundles/
sudo setfacl -m u:$current_user:rwx /srv/activities

echo "Creating directory to store temporary bundles"
sudo mkdir -p /tmp/bundles

sudo setfacl -m u:$current_user:rwx /tmp/bundles

echo "Done "