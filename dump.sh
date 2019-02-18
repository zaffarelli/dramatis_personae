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

echo "Dumping user data..."
python3 manage.py dumpdata collector.Skill --format xml --output backup/skills.xml
python3 manage.py dumpdata collector.Talent --format xml --output backup/talents.xml
python3 manage.py dumpdata collector.BlessingCurse --format xml --output backup/blessingcurses.xml
python3 manage.py dumpdata collector.BeneficeAffliction --format xml --output backup/beneficeafflictions.xml
python3 manage.py dumpdata collector.Character --format xml --output backup/characters.xml
