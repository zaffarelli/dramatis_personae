# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash

echo -e "\e[0;34mFlushing database...\e[0;m"
python3 manage.py flush
echo -e "\e[0;34m...done\e[0;m"

echo -e "\e[0;34mLoading reference data...\e[0;m"
python manage.py loaddata backup/reference/20221026/weapon_ref.xml
python manage.py loaddata backup/reference/20221026/skill_ref.xml
python manage.py loaddata backup/reference/20221026/armor_ref.xml
python manage.py loaddata backup/reference/20221026/shield_ref.xml
python manage.py loaddata backup/reference/20221026/talent_ref.xml
python manage.py loaddata backup/reference/20221026/specie.xml
python manage.py loaddata backup/reference/20221026/ritualref.xml
python manage.py loaddata backup/reference/20221026/gear.xml

echo -e "\e[1;35mLoading custom data...\e[0;m"
python manage.py loaddata backup/reference/20221026/blessing_curse_ref.xml
python manage.py loaddata backup/reference/20221026/benefice_affliction_ref.xml
python manage.py loaddata backup/reference/20221026/blessing_curse_modificator.xml
python manage.py loaddata backup/reference/20221026/benefice_affliction_modificator.xml
python manage.py loaddata backup/reference/20221026/skill_modificator.xml
python manage.py loaddata backup/reference/20221026/tour_of_duty_ref.xml

echo -e "\e[0;35m- Starship Reference...\e[0;m"
python manage.py loaddata backup/custom/20221026/ship_system.xml
python manage.py loaddata backup/custom/20221026/ship_section.xml
python manage.py loaddata backup/custom/20221026/ship_ref.xml

echo -e "\e[0;34m...done\e[0;m"











