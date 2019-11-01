#!/bin/bash

echo "Going to install Overview, an Apache/WSGI server, and all prerequisites for production"
echo "The Git must have been cloned/copied in /srv/overview"
echo "And the desired commit/branch/tag must have been checked out (before launching this script)"
echo

read -p "Confirm that the Git has been cloned/copied into /srv/overview ? (y/n) " answer
if [ "$answer" != "y" ]
then
    echo "Exiting"
    exit 1
fi

read -p "Confirm the desired commit/branch/tag has been checked out? (y/n) " answer
if [ "$answer" != "y" ]
then
    echo "Exiting"
    exit 1
fi

echo "Installing Apache, Postgres, and prerequisites..."

# note: libldap2-dev libsasl2-dev are prereqs of module python-ldap
apt udpate && apt install -y postgresql apache2 libapache2-mod-wsgi-py3 python3-pip python3-venv libldap2-dev libsasl2-dev

echo "Installing apache server and prerequisites... Done"


echo "Installing Python modules..."

python3 -m venv /srv/overview/venv/dev_overview
source /srv/overview/venv/dev_overview/bin/activate

pip3 install -r /srv/overview/requirements/requirements.txt

echo "Installing Python modules... Done"


echo "Configuring Apache..."

a2enmod wsgi
cp /srv/overview/deployment/apache/overview.conf /etc/apache2/sites-available
a2dissite 000-default
a2ensite overview

# Make sure Apache support UTF-8
sed -i -e "s/export LANG=C/export LANG=C.UTF-8/g" /etc/apache2/envvars

service apache2 restart

echo "Configuring Apache... Done"


read -p "Create database? Do this only for the first install as it will DROP existing database (y/n) " answer
if [ "$answer" = "y" ]
then
    read -p "ANY EXISTING DATABASE IS GOING TO BE COMPLETELY ERASED. Confirm? (y/n) " answer
    if [ "$answer" = "y" ]
    then
        # deep magic for getting Postgres short version; to be later used to find config files
        # example: this will return "9.6" for Postgres 9.6.10. That will later be used to find file "/etc/postgresql/9.6/main/pg_hba.conf"
        psqlversion=`psql -V | sed -E "s/.*([0-9]+\.[0-9]+)\.[0-9]+/\1/g"`
        
        # test if pg_hba.conf has already been configured
        pg_hba_configured=`grep "local overview overview password" /etc/postgresql/$psqlversion/main/pg_hba.conf`
        if [ "pg_hba_configured" = "" ]
        then
            # allow any local connection on Postgres, provided the user has a postgre password (no need to have a system account)
            sed -i -e "s/# Put your actual configuration here/# Put your actual configuration here\nlocal overview overview password/g" /etc/postgresql/$psqlversion/main/pg_hba.conf
        fi
        
        echo "Backing up database (just in case)..."
        sudo -i -u postgres pg_dump -d overview > /srv/overview/database-backup-before-erase.sql
        echo "Backing up database... Done"
        
        echo "Creating and initializing database..."
        USR="overview"
        PWD="overview"
        DB="overview"
        
        sudo -i -u postgres psql -c "DROP USER IF EXISTS $USR;"
        sudo -i -u postgres psql -c "CREATE USER $USR WITH PASSWORD '$PWD';"
        
        sudo -i -u postgres psql -c "DROP DATABASE IF EXISTS $DB;"
        sudo -i -u postgres psql -c "DROP DATABASE IF EXISTS test_$DB;"
        sudo -i -u postgres psql -c "CREATE DATABASE $DB OWNER overview;"

        sudo -i -u postgres psql -c "DROP USER IF EXISTS $USR;"
        sudo -i -u postgres psql -c "CREATE USER $USR WITH PASSWORD '$PWD';"
        sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB TO $USR;"
        echo "Creating and initiating database... Done"
    fi
fi

echo "Migrating database and static files..."

python3 manage.py makemigrations common_features
python3 manage.py makemigrations overview_features
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear

echo "Migrating database and static files... Done"

read -p "Populate database? Do this only for the first install as it will MERGE DATA with existing database (y/n) " answer
if [ "$answer" = "y" ]
then
    read -p "ANY EXISTING DATABASE IS GOING TO BE ADDED SOME DUMMY DATA. Confirm? (y/n) " answer
    if [ "$answer" = "y" ]
    then
        python3 manage.py populate_prod
        mkdir -p /srv/overview/overview/medias
        cp -ru /srv/overview/overview/default_medias/* /srv/overview/overview/medias/
        chmod -R a+w overview/medias/
    fi
fi
