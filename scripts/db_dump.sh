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
#python manage.py dumpdata scenarist.QuizzQuestion --format yaml --output backup/custom/$1/quizzquestion.yml
#python manage.py dumpdata scenarist.QuizzAnswer --format yaml --output backup/custom/$1/quizzanswer.yml
#python manage.py dumpdata scenarist.Quizz --format yaml --output backup/custom/$1/quizz.yml
python manage.py dumpdata scenarist.Epic --format yaml --output backup/custom/$1/epic.yml
python manage.py dumpdata scenarist.Drama --format yaml --output backup/custom/$1/drama.yml
python manage.py dumpdata scenarist.Act --format yaml --output backup/custom/$1/act.yml
python manage.py dumpdata scenarist.Event --format yaml --output backup/custom/$1/event.yml
python manage.py dumpdata scenarist.Card --format yaml --output backup/custom/$1/card.yml
python manage.py dumpdata scenarist.Backlog --format yaml --output backup/custom/$1/backlog.yml
python manage.py dumpdata scenarist.Adventure --format yaml --output backup/custom/$1/adventure.yml
python manage.py dumpdata scenarist.Scene --format yaml --output backup/custom/$1/scene.yml
python manage.py dumpdata scenarist.Scheme --format yaml --output backup/custom/$1/scheme.yml



python manage.py dumpdata collector.RpgSystem --format yaml --output backup/custom/$1/rpg_system.yml


echo -e "\e[1;35mCOLLECTOR...\e[0;m"
echo -e "\e[0;35m- Collector References\e[0;m"
python manage.py dumpdata collector.ArmorRef --format yaml --output backup/reference/$1/armor_ref.yml
python manage.py dumpdata collector.BeneficeAfflictionRef --format yaml --output backup/reference/$1/benefice_affliction_ref.yml
python manage.py dumpdata collector.BlessingCurseRef --format yaml --output backup/reference/$1/blessing_curse_ref.yml
python manage.py dumpdata collector.Cyberfeature --format yaml --output backup/reference/$1/cyberfeature.yml
python manage.py dumpdata collector.CyberwareRef --format yaml --output backup/reference/$1/cyberware_ref.yml
python manage.py dumpdata collector.Gear --format yaml --output backup/reference/$1/gear.yml
python manage.py dumpdata collector.RitualRef --format yaml --output backup/reference/$1/ritualref.yml
python manage.py dumpdata collector.SkillRef --format yaml --output backup/reference/$1/skill_ref.yml
python manage.py dumpdata collector.ShieldRef --format yaml --output backup/reference/$1/shield_ref.yml
python manage.py dumpdata collector.ShipSystem --format yaml --output backup/reference/$1/ship_system.yml
python manage.py dumpdata collector.ShipRef --format yaml --output backup/reference/$1/ship_ref.yml
python manage.py dumpdata collector.Specie --format yaml --output backup/reference/$1/specie.yml
python manage.py dumpdata collector.TourOfDutyRef --format yaml --output backup/reference/$1/tour_of_duty_ref.yml
python manage.py dumpdata collector.WeaponRef --format yaml --output backup/reference/$1/weapon_ref.yml
python manage.py dumpdata collector.AllianceRef --format yaml --output backup/reference/$1/alliance_ref.yml



echo -e "\e[0;35m- Dumping modificator data (pushed from history creation)...\e[0;m"
python manage.py dumpdata collector.BlessingCurseModificator --format yaml --output backup/reference/$1/blessing_curse_modificator.yml
python manage.py dumpdata collector.BeneficeAfflictionModificator --format yaml --output backup/reference/$1/benefice_affliction_modificator.yml
python manage.py dumpdata collector.SkillModificator --format yaml --output backup/reference/$1/skill_modificator.yml

echo -e "\e[0;35m- Dumping custo data... (pushed from customizer) \e[0;m"
python manage.py dumpdata collector.CharacterCusto --format yaml --output backup/custom/$1/character_custo.yml
python manage.py dumpdata collector.WeaponCusto --format yaml --output backup/custom/$1/weapon_custo.yml
python manage.py dumpdata collector.ShieldCusto --format yaml --output backup/custom/$1/shield_custo.yml
python manage.py dumpdata collector.ArmorCusto --format yaml --output backup/custom/$1/armor_custo.yml
python manage.py dumpdata collector.BlessingCurseCusto --format yaml --output backup/custom/$1/blessing_curse_custo.yml
python manage.py dumpdata collector.BeneficeAfflictionCusto --format yaml --output backup/custom/$1/benefice_affliction_custo.yml
python manage.py dumpdata collector.SkillCusto --format yaml --output backup/custom/$1/skill_custo.yml
python manage.py dumpdata collector.Sequence --format yaml --output backup/custom/$1/sequence.yml

echo -e "\e[0;35m- Dumping Main Data... (Resulting from miscellaneous pushes)\e[0;m"
python manage.py dumpdata collector.Campaign --format yaml --output backup/custom/$1/campaign.yml
python manage.py dumpdata collector.Skill --format yaml --output backup/custom/$1/skill.yml
python manage.py dumpdata collector.Weapon --format yaml --output backup/custom/$1/weapon.yml
python manage.py dumpdata collector.Armor --format yaml --output backup/custom/$1/armor.yml
python manage.py dumpdata collector.Shield --format yaml --output backup/custom/$1/shield.yml
python manage.py dumpdata collector.BlessingCurse --format yaml --output backup/custom/$1/blessing_curse.yml
python manage.py dumpdata collector.BeneficeAffliction --format yaml --output backup/custom/$1/benefice_affliction.yml
python manage.py dumpdata collector.TourOfDuty --format yaml --output backup/custom/$1/tour_of_duty.yml
python manage.py dumpdata collector.Character --format yaml --output backup/custom/$1/character.yml
python manage.py dumpdata collector.Bloke --format yaml --output backup/custom/$1/bloke.yml
python manage.py dumpdata collector.Loot --format yaml --output backup/custom/$1/loot.yml
#python manage.py dumpdata collector.Investigator --format yaml --output backup/custom/$1/investigator.yml
python manage.py dumpdata collector.Spaceship --format yaml --output backup/custom/$1/spaceship.yml
python manage.py dumpdata collector.Cyberware --format yaml --output backup/custom/$1/cyberware.yml

python manage.py dumpdata cartograph.System --format yaml --output backup/custom/$1/system.yml
python manage.py dumpdata cartograph.OrbitalItem --format yaml --output backup/custom/$1/orbital_item.yml

python manage.py dumpdata collector.Collection --format yaml --output backup/custom/$1/collection.yml

python manage.py dumpdata auth.User --format yaml --output backup/custom/$1/user.yml
python manage.py dumpdata auth.Group --format yaml --output backup/custom/$1/group.yml
python manage.py dumpdata collector.Profile --format yaml --output backup/custom/$1/profile.yml


echo -e "\e[1;35mMoving to fixtures...\e[0;m"
cp backup/reference/$1/* collector/fixtures/

echo -e "\e[1;35mStoring characters pictures...\e[0;m"
cp dp_media/images/f_*.jpg backup/images/$1/


echo -e "\e[1;35m...done\e[0;m"
