# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear
echo "Dumping All"
python3 manage.py dumpdata --format xml --output backup/db.xml

echo "Dumping reference data..."
python3 manage.py dumpdata collector.WeaponRef --format xml --output backup/weaponrefs.xml
python3 manage.py dumpdata collector.SkillRef --format xml --output backup/skillrefs.xml
python3 manage.py dumpdata collector.ArmorRef --format xml --output backup/armorrefs.xml
python3 manage.py dumpdata collector.ShieldRef --format xml --output backup/shieldrefs.xml
python3 manage.py dumpdata collector.BeneficeAfflictionRef --format xml --output backup/beneficeafflictionrefs.xml
python3 manage.py dumpdata collector.CastRole --format xml --output backup/castroles.xml
python3 manage.py dumpdata collector.CastProfile --format xml --output backup/castprofiles.xml
python3 manage.py dumpdata collector.CastEveryman --format xml --output backup/casteverymans.xml

echo "Dumping user data..."
python3 manage.py dumpdata collector.Skill --format xml --output backup/skills.xml
python3 manage.py dumpdata collector.Weapon --format xml --output backup/weapons.xml
python3 manage.py dumpdata collector.Armor --format xml --output backup/armors.xml
python3 manage.py dumpdata collector.Shield --format xml --output backup/shields.xml
python3 manage.py dumpdata collector.Talent --format xml --output backup/talents.xml
python3 manage.py dumpdata collector.BlessingCurse --format xml --output backup/blessingcurses.xml
python3 manage.py dumpdata collector.BeneficeAffliction --format xml --output backup/beneficeafflictions.xml
python3 manage.py dumpdata collector.Character --format xml --output backup/characters.xml

python3 manage.py dumpdata scenarist.Epic --format xml --output backup/epics.xml
python3 manage.py dumpdata scenarist.Drama --format xml --output backup/dramas.xml
python3 manage.py dumpdata scenarist.Act --format xml --output backup/acts.xml
python3 manage.py dumpdata scenarist.Event --format xml --output backup/events.xml

python3 manage.py dumpdata collector.Config --format xml --output backup/configs.xml

echo "Moving to fixtures..."
cp backup/skillrefs.xml collector/fixtures/
cp backup/castroles.xml collector/fixtures/
cp backup/castprofiles.xml collector/fixtures/
cp backup/casteverymans.xml collector/fixtures/


echo "...done"
