#!/bin/bash
clear
echo
echo -e "\e[0;35m"
echo -e "║ ╔╦╗╔═╗                              ║"
echo -e "║  ║║╠═╝  PC / CentOS 7               ║"
echo -e "║ ═╩╝╩    Deployment Script           ║"
echo -e "\e[0;m"
echo -e "If you're running this script, it is supposed to be from Fedora 30+ system on the dev system in the /srv/dramatis_personae directory where you have cloned the github repository and checked it out."
read -p "Are you sure you want to continue? (y/N) " answer
if [ "$answer" != "y" ]
then
  echo -e "\e[1;31m...cancelled.\e[0;m"
  exit 1
fi
echo
echo -e "\e[0;35mChecking Python...\e[0;m"
  sudo dnf install -y python3 python3-pip python3-devel gcc-c++ libjpeg libjpeg-devel
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mChecking apache...\e[0;m"
  sudo dnf install -y httpd httpd-devel nmap mod_wsgi
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mInstalling Python modules and virtual environment...\e[0;m"
    rm -rf venv/prod
    python -m venv /srv/dramatis_personae/venv/prod
echo -e "\e[0;34m   --> Venv created\e[0;m"
    source /srv/dramatis_personae/venv/prod/bin/activate
echo -e "\e[0;34m   --> Venv sourced\e[0;m"
    pip install --upgrade pip
echo -e "\e[0;34m   --> Pip upgraded\e[0;m"
    pip install -r requirements/local_prod.txt
echo -e "\e[0;34m   --> Venv packages installed\e[0;m"
    sudo mkdir logs
echo -e "\e[0;34m   --> Log dir\e[0;m"
    sudo systemctl stop httpd
    sudo touch logs/dramatis_personae.log
    sudo chown -R apache: logs/
    sudo chmod -R 755 logs/
    sudo systemctl start httpd
echo -e "\e[0;34m   --> Log file\e[0;m"
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mConfiguring Apache...\e[0;m"
    sudo systemctl stop httpd
    sudo cp /srv/dramatis_personae/scripts/deploy/httpd_dp.conf /etc/httpd/conf.d/
    sudo systemctl start httpd
    sudo systemctl enable httpd
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35mDatabase setup...\e[0;m"
    sudo systemctl stop httpd
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --no-input --clear
    sudo chown -R apache: /srv/dramatis_personae/dp_static/
    sudo chmod -R 755 /srv/dramatis_personae/dp_static/
    sudo systemctl start httpd
echo -e "\e[0;35mDo we use... \e[0;m"
echo -e "\e[0;35m a) ...the current database?\e[0;m"
echo -e "\e[0;35m b) ...a blank database? \e[0;m"
echo -e "\e[0;35m c) ...a rebuilt database? \e[0;m"
read -p "...? (A/b/c) " answer
if [ "$answer" == "b" ]
then
    scripts/db_load_initial.sh
    scripts/test.sh
else
    if [ "$answer" == "c" ]
    then
        scripts/db_load_custom.sh
        scripts/test.sh
    else
      echo -e "\e[0;35mUsing db in its current state.\e[0;m"
    fi
fi
echo -e "\e[0;35m...done.\e[0;m"
echo
echo -e "\e[0;35m* * * * * OK!!! .\e[0;m"
