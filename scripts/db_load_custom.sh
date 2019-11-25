# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash

echo -e "\e[0;36mLoading reference data\e[0;m"
scripts/db_load_initial.sh
echo -e "\e[0;36m...done\e[0;m"

echo -e "\e[0;36mLoading custom data\e[0;m"
python3 manage.py loaddata backup/custom/epic.xml
python3 manage.py loaddata backup/custom/drama.xml
python3 manage.py loaddata backup/custom/act.xml
python3 manage.py loaddata backup/custom/event.xml
python3 manage.py loaddata backup/custom/character.xml
python3 manage.py loaddata backup/custom/skill.xml
python3 manage.py loaddata backup/custom/weapon.xml
python3 manage.py loaddata backup/custom/armor.xml
python3 manage.py loaddata backup/custom/shield.xml
python3 manage.py loaddata backup/custom/talent.xml
python3 manage.py loaddata backup/custom/blessingcurse.xml
python3 manage.py loaddata backup/custom/beneficeaffliction.xml
python3 manage.py loaddata backup/custom/tourofduty.xml
python3 manage.py loaddata backup/custom/config.xml

echo -e "\e[0;36mDone\e[0;m"
