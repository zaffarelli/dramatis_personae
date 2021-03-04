# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

rm -f backup/custom/*
rm -f backup/reference/*


echo -e "\e[1;35mSCENARIST...\e[0;m"
echo -e "\e[0;35m- Dumping Main Data...\e[0;m"
python manage.py dumpdata scenarist.QuizzQuestion --format xml --output backup/custom/quizzquestion.xml
python manage.py dumpdata scenarist.QuizzAnswer --format xml --output backup/custom/quizzanswer.xml
python manage.py dumpdata scenarist.Quizz --format xml --output backup/custom/quizz.xml
python manage.py dumpdata scenarist.Epic --format xml --output backup/custom/epic.xml
python manage.py dumpdata scenarist.Drama --format xml --output backup/custom/drama.xml
python manage.py dumpdata scenarist.Act --format xml --output backup/custom/act.xml
python manage.py dumpdata scenarist.Event --format xml --output backup/custom/event.xml


python manage.py dumpdata collector.RpgSystem --format xml --output backup/custom/rpg_system.xml


echo -e "\e[1;35mCOLLECTOR...\e[0;m"
echo -e "\e[0;35m- Collector References\e[0;m"
python manage.py dumpdata collector.ArmorRef --format xml --output backup/reference/armor_ref.xml
python manage.py dumpdata collector.BeneficeAfflictionRef --format xml --output backup/reference/benefice_affliction_ref.xml
python manage.py dumpdata collector.BlessingCurseRef --format xml --output backup/reference/blessing_curse_ref.xml
python manage.py dumpdata collector.Cyberfeature --format xml --output backup/reference/cyberfeature.xml
python manage.py dumpdata collector.CyberwareRef --format xml --output backup/reference/cyberware_ref.xml
python manage.py dumpdata collector.Gear --format xml --output backup/reference/gear.xml
python manage.py dumpdata collector.RitualRef --format xml --output backup/reference/ritualref.xml
python manage.py dumpdata collector.SkillRef --format xml --output backup/reference/skill_ref.xml
python manage.py dumpdata collector.ShieldRef --format xml --output backup/reference/shield_ref.xml
python manage.py dumpdata collector.ShipSection --format xml --output backup/reference/ship_section.xml
python manage.py dumpdata collector.ShipSystem --format xml --output backup/reference/ship_system.xml
python manage.py dumpdata collector.ShipRef --format xml --output backup/reference/ship_ref.xml
python manage.py dumpdata collector.Specie --format xml --output backup/reference/specie.xml
python manage.py dumpdata collector.TourOfDutyRef --format xml --output backup/reference/tour_of_duty_ref.xml
python manage.py dumpdata collector.WeaponRef --format xml --output backup/reference/weapon_ref.xml
python manage.py dumpdata collector.Coc7Occupation --format xml --output backup/reference/coc7_occupation.xml
python manage.py dumpdata collector.AllianceRef --format xml --output backup/reference/alliance_ref.xml

echo -e "\e[0;35m- Dumping modificator data (pushed from history creation)...\e[0;m"
python manage.py dumpdata collector.BlessingCurseModificator --format xml --output backup/reference/blessing_curse_modificator.xml
python manage.py dumpdata collector.BeneficeAfflictionModificator --format xml --output backup/reference/benefice_affliction_modificator.xml
python manage.py dumpdata collector.SkillModificator --format xml --output backup/reference/skill_modificator.xml

echo -e "\e[0;35m- Dumping custo data... (pushed from customizer) \e[0;m"
python manage.py dumpdata collector.CharacterCusto --format xml --output backup/custom/character_custo.xml
python manage.py dumpdata collector.WeaponCusto --format xml --output backup/custom/weapon_custo.xml
python manage.py dumpdata collector.ShieldCusto --format xml --output backup/custom/shield_custo.xml
python manage.py dumpdata collector.ArmorCusto --format xml --output backup/custom/armor_custo.xml
python manage.py dumpdata collector.BlessingCurseCusto --format xml --output backup/custom/blessing_curse_custo.xml
python manage.py dumpdata collector.BeneficeAfflictionCusto --format xml --output backup/custom/benefice_affliction_custo.xml
python manage.py dumpdata collector.SkillCusto --format xml --output backup/custom/skill_custo.xml

echo -e "\e[0;35m- Dumping Main Data... (Resulting from miscellaneous pushes)\e[0;m"
python manage.py dumpdata collector.Campaign --format xml --output backup/custom/campaign.xml
python manage.py dumpdata collector.Skill --format xml --output backup/custom/skill.xml
python manage.py dumpdata collector.Weapon --format xml --output backup/custom/weapon.xml
python manage.py dumpdata collector.Armor --format xml --output backup/custom/armor.xml
python manage.py dumpdata collector.Shield --format xml --output backup/custom/shield.xml
python manage.py dumpdata collector.BlessingCurse --format xml --output backup/custom/blessing_curse.xml
python manage.py dumpdata collector.BeneficeAffliction --format xml --output backup/custom/benefice_affliction.xml
python manage.py dumpdata collector.TourOfDuty --format xml --output backup/custom/tour_of_duty.xml
python manage.py dumpdata collector.Character --format xml --output backup/custom/character.xml
python manage.py dumpdata collector.Bloke --format xml --output backup/custom/bloke.xml
python manage.py dumpdata collector.Loot --format xml --output backup/custom/loot.xml
python manage.py dumpdata collector.Investigator --format xml --output backup/custom/investigator.xml
python manage.py dumpdata collector.Spaceship --format xml --output backup/custom/spaceship.xml
python manage.py dumpdata collector.Cyberware --format xml --output backup/custom/cyberware.xml

python manage.py dumpdata cartograph.System --format xml --output backup/custom/system.xml
python manage.py dumpdata cartograph.OrbitalItem --format xml --output backup/custom/orbital_item.xml

python manage.py dumpdata auth.User --format xml --output backup/custom/user.xml
python manage.py dumpdata auth.Group --format xml --output backup/custom/group.xml
python manage.py dumpdata collector.Profile --format xml --output backup/custom/profile.xml


echo -e "\e[1;35mMoving to fixtures...\e[0;m"
cp backup/reference/* collector/fixtures/

echo -e "\e[1;35m...done\e[0;m"
