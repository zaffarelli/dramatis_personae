# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

mkdir -p backup/custom/$1/
mkdir -p backup/reference/$1/
mkdir -p backup/images/$1/

rm -f backup/custom/$1/*
rm -f backup/reference/$1/*
rm -f backup/images/$1/*
rm -f collector/fixtures/*

echo -e "\e[1;35mSCENARIST...\e[0;m"
echo -e "\e[0;35m- Dumping Main Data...\e[0;m"
python manage.py dumpdata scenarist.QuizzQuestion --format xml --output backup/custom/$1/quizzquestion.xml
python manage.py dumpdata scenarist.QuizzAnswer --format xml --output backup/custom/$1/quizzanswer.xml
python manage.py dumpdata scenarist.Quizz --format xml --output backup/custom/$1/quizz.xml
python manage.py dumpdata scenarist.Epic --format xml --output backup/custom/$1/epic.xml
python manage.py dumpdata scenarist.Drama --format xml --output backup/custom/$1/drama.xml
python manage.py dumpdata scenarist.Act --format xml --output backup/custom/$1/act.xml
python manage.py dumpdata scenarist.Event --format xml --output backup/custom/$1/event.xml
python manage.py dumpdata scenarist.Card --format xml --output backup/custom/$1/card.xml
python manage.py dumpdata scenarist.Backlog --format xml --output backup/custom/$1/backlog.xml
python manage.py dumpdata scenarist.Adventure --format xml --output backup/custom/$1/adventure.xml
python manage.py dumpdata scenarist.Scene --format xml --output backup/custom/$1/scene.xml
python manage.py dumpdata scenarist.Scheme --format xml --output backup/custom/$1/scheme.xml


python manage.py dumpdata collector.RpgSystem --format xml --output backup/custom/$1/rpg_system.xml


echo -e "\e[1;35mCOLLECTOR...\e[0;m"
echo -e "\e[0;35m- Collector References\e[0;m"
python manage.py dumpdata collector.ArmorRef --format xml --output backup/reference/$1/armor_ref.xml
python manage.py dumpdata collector.BeneficeAfflictionRef --format xml --output backup/reference/$1/benefice_affliction_ref.xml
python manage.py dumpdata collector.BlessingCurseRef --format xml --output backup/reference/$1/blessing_curse_ref.xml
python manage.py dumpdata collector.Cyberfeature --format xml --output backup/reference/$1/cyberfeature.xml
python manage.py dumpdata collector.CyberwareRef --format xml --output backup/reference/$1/cyberware_ref.xml
python manage.py dumpdata collector.Gear --format xml --output backup/reference/$1/gear.xml
python manage.py dumpdata collector.RitualRef --format xml --output backup/reference/$1/ritualref.xml
python manage.py dumpdata collector.SkillRef --format xml --output backup/reference/$1/skill_ref.xml
python manage.py dumpdata collector.ShieldRef --format xml --output backup/reference/$1/shield_ref.xml
python manage.py dumpdata collector.ShipSystem --format xml --output backup/reference/$1/ship_system.xml
python manage.py dumpdata collector.ShipRef --format xml --output backup/reference/$1/ship_ref.xml
python manage.py dumpdata collector.Specie --format xml --output backup/reference/$1/specie.xml
python manage.py dumpdata collector.TourOfDutyRef --format xml --output backup/reference/$1/tour_of_duty_ref.xml
python manage.py dumpdata collector.WeaponRef --format xml --output backup/reference/$1/weapon_ref.xml
python manage.py dumpdata collector.AllianceRef --format xml --output backup/reference/$1/alliance_ref.xml

echo -e "\e[0;35m- Dumping modificator data (pushed from history creation)...\e[0;m"
python manage.py dumpdata collector.BlessingCurseModificator --format xml --output backup/reference/$1/blessing_curse_modificator.xml
python manage.py dumpdata collector.BeneficeAfflictionModificator --format xml --output backup/reference/$1/benefice_affliction_modificator.xml
python manage.py dumpdata collector.SkillModificator --format xml --output backup/reference/$1/skill_modificator.xml

echo -e "\e[0;35m- Dumping custo data... (pushed from customizer) \e[0;m"
python manage.py dumpdata collector.CharacterCusto --format xml --output backup/custom/$1/character_custo.xml
python manage.py dumpdata collector.WeaponCusto --format xml --output backup/custom/$1/weapon_custo.xml
python manage.py dumpdata collector.ShieldCusto --format xml --output backup/custom/$1/shield_custo.xml
python manage.py dumpdata collector.ArmorCusto --format xml --output backup/custom/$1/armor_custo.xml
python manage.py dumpdata collector.BlessingCurseCusto --format xml --output backup/custom/$1/blessing_curse_custo.xml
python manage.py dumpdata collector.BeneficeAfflictionCusto --format xml --output backup/custom/$1/benefice_affliction_custo.xml
python manage.py dumpdata collector.SkillCusto --format xml --output backup/custom/$1/skill_custo.xml
python manage.py dumpdata collector.Sequence --format xml --output backup/custom/$1/sequence.xml

echo -e "\e[0;35m- Dumping Main Data... (Resulting from miscellaneous pushes)\e[0;m"
python manage.py dumpdata collector.Campaign --format xml --output backup/custom/$1/campaign.xml
python manage.py dumpdata collector.Skill --format xml --output backup/custom/$1/skill.xml
python manage.py dumpdata collector.Weapon --format xml --output backup/custom/$1/weapon.xml
python manage.py dumpdata collector.Armor --format xml --output backup/custom/$1/armor.xml
python manage.py dumpdata collector.Shield --format xml --output backup/custom/$1/shield.xml
python manage.py dumpdata collector.BlessingCurse --format xml --output backup/custom/$1/blessing_curse.xml
python manage.py dumpdata collector.BeneficeAffliction --format xml --output backup/custom/$1/benefice_affliction.xml
python manage.py dumpdata collector.TourOfDuty --format xml --output backup/custom/$1/tour_of_duty.xml
python manage.py dumpdata collector.Character --format xml --output backup/custom/$1/character.xml
python manage.py dumpdata collector.Bloke --format xml --output backup/custom/$1/bloke.xml
python manage.py dumpdata collector.Loot --format xml --output backup/custom/$1/loot.xml
#python manage.py dumpdata collector.Investigator --format xml --output backup/custom/$1/investigator.xml
python manage.py dumpdata collector.Spaceship --format xml --output backup/custom/$1/spaceship.xml
python manage.py dumpdata collector.Cyberware --format xml --output backup/custom/$1/cyberware.xml

python manage.py dumpdata cartograph.System --format xml --output backup/custom/$1/system.xml
python manage.py dumpdata cartograph.OrbitalItem --format xml --output backup/custom/$1/orbital_item.xml

python manage.py dumpdata auth.User --format xml --output backup/custom/$1/user.xml
python manage.py dumpdata auth.Group --format xml --output backup/custom/$1/group.xml
python manage.py dumpdata collector.Profile --format xml --output backup/custom/$1/profile.xml


echo -e "\e[1;35mMoving to fixtures...\e[0;m"
cp backup/reference/$1/* collector/fixtures/

echo -e "\e[1;35mStoring characters pictures...\e[0;m"
cp dp_media/images/f_*.jpg backup/images/$1/


echo -e "\e[1;35m...done\e[0;m"
