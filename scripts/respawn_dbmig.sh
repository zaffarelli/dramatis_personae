# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

echo -e "\e[0;35mRemoving Migrations Directories of project Apps...\e[0;m"
rm zapp/migrations/0*.py
rm scenarist/migrations/0*.py
rm cartograph/migrations/0*.py
rm optimizer/migrations/0*.py
rm collector/migrations/0*.py


echo -e "\e[1;35m...Zapp \e[0;m"
python ./manage.py migrate zapp --prune
python ./manage.py makemigrations zapp
python ./manage.py migrate zapp

echo -e "\e[1;35m...Cartograph \e[0;m"
python ./manage.py migrate cartograph --prune
python ./manage.py makemigrations cartograph
python ./manage.py migrate cartograph

echo -e "\e[1;35m...Scenarist \e[0;m"
python ./manage.py migrate scenarist --prune
python ./manage.py makemigrations scenarist
python ./manage.py migrate scenarist

echo -e "\e[1;35m...Optimizer \e[0;m"
python ./manage.py migrate optimizer --prune
python ./manage.py makemigrations optimizer
python ./manage.py migrate optimizer


echo -e "\e[1;35m...Optimizer \e[0;m"
python ./manage.py migrate collector --prune
python ./manage.py makemigrations collector
python ./manage.py migrate collector

echo -e "\e[1;35m...Global test migrate\e[0;m"
python ./manage.py makemigrations
python ./manage.py migrate

echo -e "\e[1;35m...done\e[0;m"