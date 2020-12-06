# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash

echo -e "\e[0;34mFlushing database...\e[0;m"
python3 manage.py flush
echo -e "\e[0;34m...done\e[0;m"

echo -e "\e[0;34mLoading reference data...\e[0;m"
python manage.py loaddata backup/reference/weapon_ref.xml
python manage.py loaddata backup/reference/skill_ref.xml
python manage.py loaddata backup/reference/armor_ref.xml
python manage.py loaddata backup/reference/shield_ref.xml
python manage.py loaddata backup/reference/talent_ref.xml
python manage.py loaddata backup/reference/specie.xml
python manage.py loaddata backup/reference/ritualref.xml
python manage.py loaddata backup/reference/gear.xml

echo -e "\e[1;35mLoading custom data...\e[0;m"
python manage.py loaddata backup/reference/blessing_curse_ref.xml
python manage.py loaddata backup/reference/benefice_affliction_ref.xml
python manage.py loaddata backup/reference/blessing_curse_modificator.xml
python manage.py loaddata backup/reference/benefice_affliction_modificator.xml
python manage.py loaddata backup/reference/skill_modificator.xml
python manage.py loaddata backup/reference/tour_of_duty_ref.xml

echo -e "\e[0;35m- Starship Reference...\e[0;m"
python manage.py loaddata backup/custom/ship_system.xml
python manage.py loaddata backup/custom/ship_section.xml
python manage.py loaddata backup/custom/ship_ref.xml

echo -e "\e[0;34m...done\e[0;m"











