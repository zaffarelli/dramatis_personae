#!/bin/bash
echo
echo -e "\e[0;35m"
echo -e "║ ╔╦╗╔═╗                              ║"
echo -e "║  ║║╠═╝  Raspberri PI 3B+ / CentOS 7 ║"
echo -e "║ ═╩╝╩    Deployment Script           ║"
echo -e "\e[0;m"
echo -e "If you're running this script, it is supposed to be from CentOS 7 system on a Raspberry Pi 3B+ in the /srv/dramatis_personae directory where you "
echo -e "have cloned the github repository and checked it out."
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
read -p "Do we need to install Python? (y/N) " answer
if [ "$answer" == "y" ]
then
  #sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
  yum install -y python3 python3-pip python3-devel gcc-c++ libjpeg libjpeg-devel #zlib1g-devel
else
  echo -e "\e[1;31m...cancelled.\e[0;m"
  exit 1    
fi
echo -e "\e[0;35m...done.\e[0;m"
read -p "Do we need to install Apache? (y/N) " answer
if [ "$answer" == "y" ]
then
  sudo yum install -y httpd nmap
fi
echo -e "\e[0;35m...done.\e[0;m"
echo 
echo -e "\e[0;35mInstalling Python modules and virtual environment...\e[0;m"
python3 -m venv /srv/dramatis_personae/venv/dp
source /srv/dramatis_personae/venv/dp/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements/prod.txt
touch /srv/dramatis_personae/dramatis_personae/logs/dramatis_personae.log
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mConfiguring Apache...\e[0;m"
systemctl stop httpd
cp /srv/dramatis_personae/scripts/deploy/httpd_dp.conf /etc/httpd/conf.d/
systemctl start httpd
systemctl enable httpd
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
/srv/dramatis_personae/venv/dp/bin/deactivate
echo -e "\e[0;35m* * * * *.\e[0;m"
