# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear
#echo "Dumping All"
#python3 manage.py dumpdata --format xml --output backup/db.xml

echo "Dumping reference data..."
python3 manage.py dumpdata collector.WeaponRef --format xml --output backup/reference/weaponrefs.xml
python3 manage.py dumpdata collector.SkillRef --format xml --output backup/reference/skillrefs.xml
python3 manage.py dumpdata collector.ArmorRef --format xml --output backup/reference/armorrefs.xml
python3 manage.py dumpdata collector.ShieldRef --format xml --output backup/reference/shieldrefs.xml
python3 manage.py dumpdata collector.BeneficeAfflictionRef --format xml --output backup/reference/beneficeafflictionrefs.xml
python3 manage.py dumpdata collector.CastRole --format xml --output backup/reference/castroles.xml
python3 manage.py dumpdata collector.CastProfile --format xml --output backup/reference/castprofiles.xml
python3 manage.py dumpdata collector.CastEveryman --format xml --output backup/reference/casteverymans.xml

echo "Dumping user data..."
python3 manage.py dumpdata collector.Skill --format xml --output backup/custom/skills.xml
python3 manage.py dumpdata collector.Weapon --format xml --output backup/custom/weapons.xml
python3 manage.py dumpdata collector.Armor --format xml --output backup/custom/armors.xml
python3 manage.py dumpdata collector.Shield --format xml --output backup/custom/shields.xml
python3 manage.py dumpdata collector.Talent --format xml --output backup/custom/talents.xml
python3 manage.py dumpdata collector.BlessingCurse --format xml --output backup/custom/blessingcurses.xml
python3 manage.py dumpdata collector.BeneficeAffliction --format xml --output backup/custom/beneficeafflictions.xml
python3 manage.py dumpdata collector.Character --format xml --output backup/custom/characters.xml

python3 manage.py dumpdata scenarist.Epic --format xml --output backup/custom/epics.xml
python3 manage.py dumpdata scenarist.Drama --format xml --output backup/custom/dramas.xml
python3 manage.py dumpdata scenarist.Act --format xml --output backup/custom/acts.xml
python3 manage.py dumpdata scenarist.Event --format xml --output backup/custom/events.xml

python3 manage.py dumpdata collector.Config --format xml --output backup/configs.xml

echo "Moving to fixtures..."
cp backup/reference/skillrefs.xml collector/fixtures/
cp backup/reference/castroles.xml collector/fixtures/
cp backup/reference/castprofiles.xml collector/fixtures/
cp backup/reference/casteverymans.xml collector/fixtures/


echo "...done"
