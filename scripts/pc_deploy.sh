#!/bin/bash
clear
echo
echo -e "\e[0;35m"
echo -e "║ ╔╦╗╔═╗                              ║"
echo -e "║  ║║╠═╝  PC / Fedora 31              ║"
echo -e "║ ═╩╝╩    Deployment Script           ║"
echo -e "\e[0;m"
echo -e "If you're running this script, it is supposed to be from CentOS 7 system on a Raspberry Pi 3B+ in the /srv/dramatis_personae directory where you have cloned the github repository and checked it out."
read -p "Are you sure you want to continue? (y/N) " answer
if [ "$answer" != "y" ]
then
  echo -e "\e[1;31m...cancelled.\e[0;m"
  exit 1
fi
echo
echo -e "\e[0;35mChecking system updates...\e[0;m"
read -p "Do we need to check for system updates? (y/N) " answer
if [ "$answer" == "y" ]
then
  sudo yum update -y
fi
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mInstalling Python...\e[0;m"
read -p "Do we need to install Python? (y/N) " answer
if [ "$answer" == "y" ]
then
  yum install -y python3 python3-pip python3-devel gcc-c++ libjpeg libjpeg-devel #zlib1g-devel
else
  echo -e "\e[1;31m...cancelled.\e[0;m"
  exit 1
fi
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mInstalling apache...\e[0;m"
read -p "Do we need to install apache? (y/N) " answer
if [ "$answer" == "y" ]
then
  sudo yum install -y httpd httpd-devel nmap mod_wsgi
  #sudo yum install epel-release nginx -y
fi
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mInstalling Python modules and virtual environment...\e[0;m"
rm -rf venv/prod
python3 -m venv /srv/dramatis_personae/venv/prod
echo -e "\e[0;34m   --> Venv created\e[0;m"
source /srv/dramatis_personae/venv/prod/bin/activate
echo -e "\e[0;34m   --> Venv sourced\e[0;m"
pip3 install --user --upgrade pip
echo -e "\e[0;34m   --> Pip upgraded\e[0;m"
pip3 install --user -r requirements/local_prod.txt
echo -e "\e[0;34m   --> Venv packages installed\e[0;m"
mkdir /srv/dramatis_personae/dramatis_personae/logs
echo -e "\e[0;34m   --> Log dir\e[0;m"
touch /srv/dramatis_personae/dramatis_personae/logs/dramatis_personae.log
chmod 777 /srv/dramatis_personae/dramatis_personae/logs/dramatis_personae.log
echo -e "\e[0;34m   --> Log file\e[0;m"
echo -e "\e[0;35m...done.\e[0;m"
echo

#export DJANGO_SETTINGS_MODULE=dramatis_personae.settings.prod

#uwsgi --module=dramatis_personae.wsgi:application --env=DJANGO_SETTINGS_MODULE=dramatis_personae.settings.prod --master --pidfile=/tmp/project-master.pid --http=0.0.0.0:8088 --uid=1000 --virtualenv=/home/zaffarelli/Projects/github/dramatis_personae/venv/dp



echo -e "\e[0;35mConfiguring NGINX...\e[0;m"
systemctl stop httpd
cp /srv/dramatis_personae/scripts/deploy/httpd_dp.conf /etc/httpd/conf.d/
systemctl start httpd
systemctl enable httpd
#sudo ln -s /srv/dramatis_personae/config/nginx.conf /etc/nginx/conf.d/dramatis_personae.conf
#uwsgi --ini config/uwsgi.ini
sudo systemctl restart nginx
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mDatabase setup...\e[0;m"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear
read -p "Do we use a blank database? (y/N) " answer
if [ "$answer" == "y" ]
then
  scripts/db_load_initial.sh
  scripts/test.sh
else
  scripts/db_load_custom.sh
  scripts/test.sh
fi
echo -e "\e[0;35m...done.\e[0;m"
echo

echo -e "\e[0;35m* * * * *.\e[0;m"
