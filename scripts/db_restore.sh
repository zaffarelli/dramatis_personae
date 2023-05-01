# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

echo -e "\e[0;34mFlushing database...\e[0;m"
python3 manage.py flush

echo -e "\e[1;35mCOLLECTOR...\e[0;m"
echo -e "\e[0;35m- Restoring references data\e[0;m"
python manage.py loaddata backup/reference/$1/armor_ref.xml
echo -e "\e[0;35m- BA\e[0;m"
python manage.py loaddata backup/reference/$1/benefice_affliction_ref.xml
python manage.py loaddata backup/reference/$1/blessing_curse_ref.xml
python manage.py loaddata backup/reference/$1/cyberfeature.xml
python manage.py loaddata backup/reference/$1/cyberware_ref.xml
python manage.py loaddata backup/reference/$1/gear.xml
python manage.py loaddata backup/reference/$1/skill_ref.xml
python manage.py loaddata backup/reference/$1/shield_ref.xml
python manage.py loaddata backup/reference/$1/ship_system.xml
python manage.py loaddata backup/reference/$1/ship_ref.xml
python manage.py loaddata backup/reference/$1/specie.xml
python manage.py loaddata backup/reference/$1/tour_of_duty_ref.xml
python manage.py loaddata backup/reference/$1/weapon_ref.xml
python manage.py loaddata backup/reference/$1/alliance_ref.xml

python manage.py loaddata backup/reference/$1/ritualref.xml

read -rsp $'Press any key to continue...\n' -n1 key

echo -e "\e[1;35mGLOBAL...\e[0;m"
echo -e "\e[0;35m- Restoring Groups, Users and RPG systems...\e[0;m"
python manage.py loaddata backup/custom/$1/group.xml
python manage.py loaddata backup/custom/$1/user.xml
python manage.py loaddata backup/custom/$1/rpg_system.xml

read -rsp $'Press any key to continue...\n' -n1 key

echo -e "\e[1;35mSCENARIST...\e[0;m"
echo -e "\e[0;35m- Restoring Main Data...\e[0;m"
#python manage.py loaddata backup/custom/$1/epic.xml
#python manage.py loaddata backup/custom/$1/drama.xml
#python manage.py loaddata backup/custom/$1/act.xml
#python manage.py loaddata backup/custom/$1/event.xml
python manage.py loaddata backup/custom/$1/card.xml
#python manage.py loaddata backup/custom/$1/adventure.xml
#python manage.py loaddata backup/custom/$1/backlog.xml
#python manage.py loaddata backup/custom/$1/scene.xml
#python manage.py loaddata backup/custom/$1/scheme.xml

#read -p "> Press any key to continue..."
#
#echo -e "\e[0;35m- Restoring Campaigns...\e[0;m"
#python manage.py loaddata backup/custom/$1/campaign.xml
#
#read -p "> Press any key to continue..."
#
#echo -e "\e[0;35m- Restoring modificator data (pushed from history creation)...\e[0;m"
#python manage.py loaddata backup/reference/$1/blessing_curse_modificator.xml
#python manage.py loaddata backup/reference/$1/benefice_affliction_modificator.xml
#python manage.py loaddata backup/reference/$1/skill_modificator.xml
#
#read -p "> Press any key to continue..."
#
#echo -e "\e[0;35m- Restoring Main Data... (Resulting from miscellaneous pushes)\e[0;m"
#python manage.py loaddata backup/custom/$1/campaign.xml
#python manage.py loaddata backup/custom/$1/skill.xml
#python manage.py loaddata backup/custom/$1/weapon.xml
#python manage.py loaddata backup/custom/$1/armor.xml
#python manage.py loaddata backup/custom/$1/shield.xml
#python manage.py loaddata backup/custom/$1/blessing_curse.xml
#python manage.py loaddata backup/custom/$1/benefice_affliction.xml
#python manage.py loaddata backup/custom/$1/tour_of_duty.xml
#python manage.py loaddata backup/custom/$1/character.xml
#python manage.py loaddata backup/custom/$1/bloke.xml
#python manage.py loaddata backup/custom/$1/loot.xml
#
#python manage.py loaddata backup/custom/$1/cyberware.xml
#python manage.py loaddata backup/custom/$1/spaceship.xml
#
#read -p "> Press any key to continue..."
#
#echo -e "\e[0;35m- Restoring Systems & Orbital Items\e[0;m"
#python manage.py loaddata backup/custom/$1/system.xml
#python manage.py loaddata backup/custom/$1/orbital_item.xml
#
#read -p "> Press any key to continue..."
#
#echo -e "\e[0;35m- Restoring User Profiles\e[0;m"
#python manage.py loaddata backup/custom/$1/profile.xml
#
#read -p "> Press any key to continue..."
#echo -e "\e[0;35m- Restoring custo data... (pushed from customizer) \e[0;m"
#python manage.py loaddata backup/custom/$1/character_custo.xml
#python manage.py loaddata backup/custom/$1/weapon_custo.xml
#python manage.py loaddata backup/custom/$1/shield_custo.xml
#python manage.py loaddata backup/custom/$1/armor_custo.xml
#python manage.py loaddata backup/custom/$1/blessing_curse_custo.xml
#python manage.py loaddata backup/custom/$1/benefice_affliction_custo.xml
#python manage.py loaddata backup/custom/$1/skill_custo.xml
#python manage.py loaddata backup/custom/$1/sequence.xml
#python manage.py loaddata backup/custom/$1/collection.xml


echo -e "\e[1;35m...done\e[0;m"
