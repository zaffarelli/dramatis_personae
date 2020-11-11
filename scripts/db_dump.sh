# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

echo -e "\e[1;35mDumping reference data...\e[0;m"
echo -e "\e[0;35m- Collector Refs\e[0;m"
python3 manage.py dumpdata collector.WeaponRef --format xml --output backup/reference/weapon_ref.xml
python3 manage.py dumpdata collector.SkillRef --format xml --output backup/reference/skill_ref.xml
python3 manage.py dumpdata collector.ArmorRef --format xml --output backup/reference/armor_ref.xml
python3 manage.py dumpdata collector.ShieldRef --format xml --output backup/reference/shield_ref.xml
python3 manage.py dumpdata collector.TalentRef --format xml --output backup/reference/talent_ref.xml
python3 manage.py dumpdata collector.Specie --format xml --output backup/reference/specie.xml
python3 manage.py dumpdata collector.RitualRef --format xml --output backup/reference/ritualref.xml
python3 manage.py dumpdata collector.Gear --format xml --output backup/reference/gear.xml

echo -e "\e[1;35mDumping custom data...\e[0;m"
echo -e "\e[0;35m- Tours of Duty Reference...\e[0;m"
python3 manage.py dumpdata collector.BlessingCurseRef --format xml --output backup/reference/blessing_curse_ref.xml
python3 manage.py dumpdata collector.BeneficeAfflictionRef --format xml --output backup/reference/benefice_affliction_ref.xml
python3 manage.py dumpdata collector.BlessingCurseModificator --format xml --output backup/reference/blessing_curse_modificator.xml
python3 manage.py dumpdata collector.BeneficeAfflictionModificator --format xml --output backup/reference/benefice_affliction_modificator.xml
python3 manage.py dumpdata collector.SkillModificator --format xml --output backup/reference/skill_modificator.xml
python3 manage.py dumpdata collector.TourOfDutyRef --format xml --output backup/reference/tour_of_duty_ref.xml

echo -e "\e[0;35m- Starship Reference...\e[0;m"
python3 manage.py dumpdata collector.ShipSystem --format xml --output backup/custom/ship_system.xml
python3 manage.py dumpdata collector.ShipSection --format xml --output backup/custom/ship_section.xml
python3 manage.py dumpdata collector.ShipRef --format xml --output backup/custom/ship_ref.xml

echo -e "\e[0;35m- Main data...\e[0;m"
python3 manage.py dumpdata collector.Skill --format xml --output backup/custom/skill.xml
python3 manage.py dumpdata collector.Weapon --format xml --output backup/custom/weapon.xml
python3 manage.py dumpdata collector.Armor --format xml --output backup/custom/armor.xml
python3 manage.py dumpdata collector.Shield --format xml --output backup/custom/shield.xml
python3 manage.py dumpdata collector.Talent --format xml --output backup/custom/talent.xml
python3 manage.py dumpdata collector.BlessingCurse --format xml --output backup/custom/blessing_curse.xml
python3 manage.py dumpdata collector.BeneficeAffliction --format xml --output backup/custom/benefice_affliction.xml
python3 manage.py dumpdata collector.TourOfDuty --format xml --output backup/custom/tour_of_duty.xml

echo -e "\e[0;35m- Customization Reference...\e[0;m"
python3 manage.py dumpdata collector.CharacterCusto --format xml --output backup/custom/character_custo.xml
python3 manage.py dumpdata collector.WeaponCusto --format xml --output backup/custom/weapon_custo.xml
python3 manage.py dumpdata collector.ShieldCusto --format xml --output backup/custom/shield_custo.xml
python3 manage.py dumpdata collector.ArmorCusto --format xml --output backup/custom/armor_custo.xml
python3 manage.py dumpdata collector.BlessingCurseCusto --format xml --output backup/custom/blessing_curse_custo.xml
python3 manage.py dumpdata collector.BeneficeAfflictionCusto --format xml --output backup/custom/benefice_affliction_custo.xml
python3 manage.py dumpdata collector.SkillCusto --format xml --output backup/custom/skill_custo.xml

echo -e "\e[0;35m- Collector Main Data...\e[0;m"
python3 manage.py dumpdata collector.Character --format xml --output backup/custom/character.xml
python3 manage.py dumpdata collector.Bloke --format xml --output backup/custom/bloke.xml
python3 manage.py dumpdata collector.Loot --format xml --output backup/custom/loot.xml
python3 manage.py dumpdata collector.System --format xml --output backup/custom/system.xml
python3 manage.py dumpdata collector.OrbitalItem --format xml --output backup/custom/orbital_item.xml

python3 manage.py dumpdata collector.Spaceship --format xml --output backup/custom/spaceship.xml
python3 manage.py dumpdata collector.Cyberfeature --format xml --output backup/custom/cyberfeature.xml
python3 manage.py dumpdata collector.CyberwareRef --format xml --output backup/custom/cyberware_ref.xml
python3 manage.py dumpdata collector.Cyberware --format xml --output backup/custom/cyberware.xml


echo -e "\e[0;35m- Scenarist Main Data...\e[0;m"
python3 manage.py dumpdata scenarist.QuizzQuestion --format xml --output backup/custom/quizzquestion.xml
python3 manage.py dumpdata scenarist.QuizzAnswer --format xml --output backup/custom/quizzanswer.xml
python3 manage.py dumpdata scenarist.Quizz --format xml --output backup/custom/quizz.xml
python3 manage.py dumpdata scenarist.Epic --format xml --output backup/custom/epic.xml
python3 manage.py dumpdata scenarist.Drama --format xml --output backup/custom/drama.xml
python3 manage.py dumpdata scenarist.Act --format xml --output backup/custom/act.xml
python3 manage.py dumpdata scenarist.Event --format xml --output backup/custom/event.xml
python3 manage.py dumpdata collector.Config --format xml --output backup/custom/config.xml

echo -e "\e[1;35mMoving to fixtures...\e[0;m"
cp backup/reference/skill_ref.xml collector/fixtures/
cp backup/reference/talent_ref.xml collector/fixtures/
cp backup/reference/specie.xml collector/fixtures/
cp backup/reference/benefice_affliction_ref.xml collector/fixtures/
cp backup/reference/blessing_curse_ref.xml collector/fixtures/
cp backup/reference/benefice_affliction_modificator.xml collector/fixtures/
cp backup/reference/blessing_curse_modificator.xml collector/fixtures/
cp backup/reference/skill_modificator.xml collector/fixtures/
cp backup/reference/tour_of_duty_ref.xml collector/fixtures/

echo -e "\e[1;35m...done\e[0;m"
