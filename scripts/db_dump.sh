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
python manage.py dumpdata scenarist.Epic --format json --output backup/custom/$1/epic.json
python manage.py dumpdata scenarist.Drama --format json --output backup/custom/$1/drama.json
python manage.py dumpdata scenarist.Act --format json --output backup/custom/$1/act.json
python manage.py dumpdata scenarist.Event --format json --output backup/custom/$1/event.json
python manage.py dumpdata scenarist.Card --format json --output backup/custom/$1/card.json
python manage.py dumpdata scenarist.Backlog --format json --output backup/custom/$1/backlog.json
python manage.py dumpdata scenarist.Adventure --format json --output backup/custom/$1/adventure.json
python manage.py dumpdata scenarist.Scene --format json --output backup/custom/$1/scene.json
python manage.py dumpdata scenarist.Scheme --format json --output backup/custom/$1/scheme.json



python manage.py dumpdata collector.RpgSystem --format json --output backup/custom/$1/rpg_system.json


echo -e "\e[1;35mCOLLECTOR...\e[0;m"
echo -e "\e[0;35m- Collector References\e[0;m"
python manage.py dumpdata collector.ArmorRef --format json --output backup/reference/$1/armor_ref.json
python manage.py dumpdata collector.BeneficeAfflictionRef --format json --output backup/reference/$1/benefice_affliction_ref.json
python manage.py dumpdata collector.BlessingCurseRef --format json --output backup/reference/$1/blessing_curse_ref.json
python manage.py dumpdata collector.Cyberfeature --format json --output backup/reference/$1/cyberfeature.json
python manage.py dumpdata collector.CyberwareRef --format json --output backup/reference/$1/cyberware_ref.json
python manage.py dumpdata collector.Gear --format json --output backup/reference/$1/gear.json
python manage.py dumpdata collector.RitualRef --format json --output backup/reference/$1/ritualref.json
python manage.py dumpdata collector.SkillRef --format json --output backup/reference/$1/skill_ref.json
python manage.py dumpdata collector.ShieldRef --format json --output backup/reference/$1/shield_ref.json
python manage.py dumpdata collector.ShipSystem --format json --output backup/reference/$1/ship_system.json
python manage.py dumpdata collector.ShipRef --format json --output backup/reference/$1/ship_ref.json
python manage.py dumpdata collector.Specie --format json --output backup/reference/$1/specie.json
python manage.py dumpdata collector.TourOfDutyRef --format json --output backup/reference/$1/tour_of_duty_ref.json
python manage.py dumpdata collector.WeaponRef --format json --output backup/reference/$1/weapon_ref.json
python manage.py dumpdata collector.AllianceRef --format json --output backup/reference/$1/alliance_ref.json



echo -e "\e[0;35m- Dumping modificator data (pushed from history creation)...\e[0;m"
python manage.py dumpdata collector.BlessingCurseModificator --format json --output backup/reference/$1/blessing_curse_modificator.json
python manage.py dumpdata collector.BeneficeAfflictionModificator --format json --output backup/reference/$1/benefice_affliction_modificator.json
python manage.py dumpdata collector.SkillModificator --format json --output backup/reference/$1/skill_modificator.json

echo -e "\e[0;35m- Dumping custo data... (pushed from customizer) \e[0;m"
python manage.py dumpdata collector.CharacterCusto --format json --output backup/custom/$1/character_custo.json
python manage.py dumpdata collector.WeaponCusto --format json --output backup/custom/$1/weapon_custo.json
python manage.py dumpdata collector.ShieldCusto --format json --output backup/custom/$1/shield_custo.json
python manage.py dumpdata collector.ArmorCusto --format json --output backup/custom/$1/armor_custo.json
python manage.py dumpdata collector.BlessingCurseCusto --format json --output backup/custom/$1/blessing_curse_custo.json
python manage.py dumpdata collector.BeneficeAfflictionCusto --format json --output backup/custom/$1/benefice_affliction_custo.json
python manage.py dumpdata collector.SkillCusto --format json --output backup/custom/$1/skill_custo.json
python manage.py dumpdata collector.Sequence --format json --output backup/custom/$1/sequence.json

echo -e "\e[0;35m- Dumping Main Data... (Resulting from miscellaneous pushes)\e[0;m"
python manage.py dumpdata collector.Campaign --format json --output backup/custom/$1/campaign.json
python manage.py dumpdata collector.Skill --format json --output backup/custom/$1/skill.json
python manage.py dumpdata collector.Weapon --format json --output backup/custom/$1/weapon.json
python manage.py dumpdata collector.Armor --format json --output backup/custom/$1/armor.json
python manage.py dumpdata collector.Shield --format json --output backup/custom/$1/shield.json
python manage.py dumpdata collector.BlessingCurse --format json --output backup/custom/$1/blessing_curse.json
python manage.py dumpdata collector.BeneficeAffliction --format json --output backup/custom/$1/benefice_affliction.json
python manage.py dumpdata collector.TourOfDuty --format json --output backup/custom/$1/tour_of_duty.json
python manage.py dumpdata collector.Character --format json --output backup/custom/$1/character.json
python manage.py dumpdata collector.Bloke --format json --output backup/custom/$1/bloke.json
python manage.py dumpdata collector.Loot --format json --output backup/custom/$1/loot.json
python manage.py dumpdata collector.Spaceship --format json --output backup/custom/$1/spaceship.json
python manage.py dumpdata collector.Cyberware --format json --output backup/custom/$1/cyberware.json

python manage.py dumpdata cartograph.System --format json --output backup/custom/$1/system.json
python manage.py dumpdata cartograph.OrbitalItem --format json --output backup/custom/$1/orbital_item.json

python manage.py dumpdata collector.Collection --format json --output backup/custom/$1/collection.json

python manage.py dumpdata auth.User --format json --output backup/custom/$1/user.json
python manage.py dumpdata auth.Group --format json --output backup/custom/$1/group.json
python manage.py dumpdata collector.Profile --format json --output backup/custom/$1/profile.json


echo -e "\e[1;35mMoving to fixtures...\e[0;m"
cp backup/reference/$1/* collector/fixtures/

echo -e "\e[1;35mStoring characters pictures...\e[0;m"
cp dp_media/images/f_*.jpg backup/images/$1/


echo -e "\e[1;35m...done\e[0;m"
