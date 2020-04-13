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
python3 manage.py loaddata backup/custom/blessing_curse.xml
python3 manage.py loaddata backup/custom/benefice_affliction.xml
python3 manage.py loaddata backup/custom/tour_of_duty.xml

python3 manage.py loaddata backup/custom/character_custo.xml
python3 manage.py loaddata backup/custom/blessing_curse_custo.xml
python3 manage.py loaddata backup/custom/benefice_affliction_custo.xml
python3 manage.py loaddata backup/custom/armor_custo.xml
python3 manage.py loaddata backup/custom/skill_custo.xml
python3 manage.py loaddata backup/custom/shield_custo.xml
python3 manage.py loaddata backup/custom/armor_custo.xml


python3 manage.py loaddata backup/custom/loot.xml
python3 manage.py loaddata backup/custom/system.xml
python3 manage.py loaddata backup/custom/config.xml

echo -e "\e[0;36mDone\e[0;m"
