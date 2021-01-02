# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

echo -e "\e[0;36mLoading reference data\e[0;m"
scripts/db_load_initial.sh
echo -e "\e[0;36m...done\e[0;m"























echo -e "\e[0;35m- Base data...\e[0;m"
python manage.py loaddata backup/custom/skill.xml
python manage.py loaddata backup/custom/weapon.xml
python manage.py loaddata backup/custom/armor.xml
python manage.py loaddata backup/custom/shield.xml
python manage.py loaddata backup/custom/talent.xml
python manage.py loaddata backup/custom/blessing_curse.xml
python manage.py loaddata backup/custom/benefice_affliction.xml
python manage.py loaddata backup/custom/tour_of_duty.xml

echo -e "\e[0;35m- Customization Reference...\e[0;m"
python manage.py loaddata backup/custom/character_custo.xml
python manage.py loaddata backup/custom/weapon_custo.xml
python manage.py loaddata backup/custom/shield_custo.xml
python manage.py loaddata backup/custom/armor_custo.xml
python manage.py loaddata backup/custom/blessing_curse_custo.xml
python manage.py loaddata backup/custom/benefice_affliction_custo.xml
python manage.py loaddata backup/custom/skill_custo.xml

echo -e "\e[0;35m- Collector Main Data\e[0;m"
python manage.py loaddata backup/custom/character.xml
python manage.py loaddata backup/custom/bloke.xml
python manage.py loaddata backup/custom/loot.xml
python manage.py loaddata backup/custom/system.xml
python manage.py loaddata backup/custom/orbital_item.xml

python manage.py loaddata backup/custom/spaceship.xml
python manage.py loaddata backup/custom/cyberfeature.xml
python manage.py loaddata backup/custom/cyberware_ref.xml
python manage.py loaddata backup/custom/cyberware.xml

echo -e "\e[0;35m- Scenarist Main Data...\e[0;m"
python manage.py loaddata backup/custom/quizzquestion.xml
python manage.py loaddata backup/custom/quizzanswer.xml
python manage.py loaddata backup/custom/quizz.xml
python manage.py loaddata backup/custom/epic.xml
python manage.py loaddata backup/custom/drama.xml
python manage.py loaddata backup/custom/act.xml
python manage.py loaddata backup/custom/event.xml
python manage.py loaddata backup/custom/campaign.xml

echo -e "\e[0;36mDone\e[0;m"
