# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

python3 manage.py flush

echo "Loading reference data..."
python3 manage.py loaddata backup/weaponrefs.xml
python3 manage.py loaddata backup/skillrefs.xml
python3 manage.py loaddata backup/armorrefs.xml
python3 manage.py loaddata backup/shieldrefs.xml
python3 manage.py loaddata backup/beneficeafflictionrefs.xml
python3 manage.py loaddata backup/castroles.xml
python3 manage.py loaddata backup/castprofiles.xml
python3 manage.py loaddata backup/casteverymans.xml

echo "Loading user data..."
python3 manage.py loaddata backup/epics.xml
python3 manage.py loaddata backup/dramas.xml
python3 manage.py loaddata backup/acts.xml
python3 manage.py loaddata backup/events.xml

python3 manage.py loaddata backup/characters.xml
python3 manage.py loaddata backup/skills.xml
python3 manage.py loaddata backup/weapons.xml
python3 manage.py loaddata backup/armors.xml
python3 manage.py loaddata backup/shields.xml
python3 manage.py loaddata backup/talents.xml
python3 manage.py loaddata backup/blessingcurses.xml
python3 manage.py loaddata backup/beneficeafflictions.xml




python3 manage.py loaddata backup/configs.xml

echo "...done"
