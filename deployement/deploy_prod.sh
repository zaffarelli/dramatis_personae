#!/bin/bash
echo "* ╔╦╗╔═╗  Dramatis Personae"
echo "*  ║║╠═╝  Raspberri PI 3B+"
echo "* ═╩╝╩    Deployment script"
echo "Going to install DRAMATIS PERSONAE, an Apache/WSGI server, and all prerequisites for production"
echo "The Git must have been cloned/copied in /srv/dramatis_personae"
echo "And the desired commit/branch/tag must have been checked out (before launching this script)"
echo
echo "Installing Python basics..."
yum update -y
yum install -y https://centos7.iuscommunity.org/ius-release.rpm
yum install -y python3 httpd python3-pip
echo "Installing Python basics... Done"
echo 
echo "Installing Python modules..."
python3 -m venv /srv/dramatis_personae/venv/dramatis_personae
source /srv/dramatis_personae/venv/dramatis_personae/bin/activate
pip3 install --upgrade pip
pip3 install -r /srv/dramatis_personae/requirements/prod.txt
echo "Installing Python modules... Done"
echo
echo "Configuring Apache..."
systemctl stop httpd
cp /srv/dramatis_personae/deployement/apache/dramatis_personae_httpd.conf /etc/httpd/conf.d/
systemctl start httpd
systemctl enable httpd
echo "Configuring Apache... Done"
echo
echo "Migrating database and static files..."
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear
echo "Migrating database and static files... Done"
echo
deactivate
echo "* Over *"
