# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

echo -e "\e[1;35mSCENARIST...\e[0;m"
echo -e "\e[0;35m- Restoring Main Data...\e[0;m"
python manage.py loaddata backup/custom/quizzquestion.xml
python manage.py loaddata backup/custom/quizzanswer.xml
python manage.py loaddata backup/custom/quizz.xml
python manage.py loaddata backup/custom/epic.xml
python manage.py loaddata backup/custom/drama.xml
python manage.py loaddata backup/custom/act.xml
python manage.py loaddata backup/custom/event.xml


echo -e "\e[1;35mCOLLECTOR...\e[0;m"
echo -e "\e[0;35m- Restoring references data\e[0;m"
python manage.py loaddata backup/reference/armor_ref.xml
python manage.py loaddata backup/reference/benefice_affliction_ref.xml
python manage.py loaddata backup/reference/blessing_curse_ref.xml
python manage.py loaddata backup/reference/cyberfeature.xml
python manage.py loaddata backup/reference/cyberware_ref.xml
python manage.py loaddata backup/reference/gear.xml
python manage.py loaddata backup/reference/ritualref.xml
python manage.py loaddata backup/reference/skill_ref.xml
python manage.py loaddata backup/reference/shield_ref.xml
python manage.py loaddata backup/reference/ship_section.xml
python manage.py loaddata backup/reference/ship_system.xml
python manage.py loaddata backup/reference/ship_ref.xml
python manage.py loaddata backup/reference/specie.xml
python manage.py loaddata backup/reference/tour_of_duty_ref.xml
python manage.py loaddata backup/reference/weapon_ref.xml

echo -e "\e[0;35m- Restoring modificator data (pushed from history creation)...\e[0;m"
python manage.py loaddata backup/reference/blessing_curse_modificator.xml
python manage.py loaddata backup/reference/benefice_affliction_modificator.xml
python manage.py loaddata backup/reference/skill_modificator.xml

echo -e "\e[0;35m- Restoring Main Data... (Resulting from miscellaneous pushes)\e[0;m"
python manage.py loaddata backup/custom/config.xml
python manage.py loaddata backup/custom/skill.xml
python manage.py loaddata backup/custom/weapon.xml
python manage.py loaddata backup/custom/armor.xml
python manage.py loaddata backup/custom/shield.xml
python manage.py loaddata backup/custom/blessing_curse.xml
python manage.py loaddata backup/custom/benefice_affliction.xml
python manage.py loaddata backup/custom/tour_of_duty.xml
python manage.py loaddata backup/custom/character.xml
python manage.py loaddata backup/custom/bloke.xml
python manage.py loaddata backup/custom/loot.xml
python manage.py loaddata backup/custom/system.xml
python manage.py loaddata backup/custom/orbital_item.xml
python manage.py loaddata backup/custom/investigator.xml
python manage.py loaddata backup/custom/spaceship.xml
python manage.py loaddata backup/custom/cyberware.xml

python manage.py loaddata backup/custom/profile.xml

echo -e "\e[0;35m- Restoring custo data... (pushed from customizer) \e[0;m"
python manage.py loaddata backup/custom/character_custo.xml
python manage.py loaddata backup/custom/weapon_custo.xml
python manage.py loaddata backup/custom/shield_custo.xml
python manage.py loaddata backup/custom/armor_custo.xml
python manage.py loaddata backup/custom/blessing_curse_custo.xml
python manage.py loaddata backup/custom/benefice_affliction_custo.xml
python manage.py loaddata backup/custom/skill_custo.xml

echo -e "\e[1;35m...done\e[0;m"
