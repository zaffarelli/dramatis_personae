# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash


scripts/db_load_initial.sh

echo "Loading reference data..."

___

echo "Loading user data..."
python3 manage.py loaddata backup/custom/epics.xml
python3 manage.py loaddata backup/custom/dramas.xml
python3 manage.py loaddata backup/custom/acts.xml
python3 manage.py loaddata backup/custom/events.xml

python3 manage.py loaddata backup/custom/characters.xml
python3 manage.py loaddata backup/custom/skills.xml
python3 manage.py loaddata backup/custom/weapons.xml
python3 manage.py loaddata backup/custom/armors.xml
python3 manage.py loaddata backup/custom/shields.xml
python3 manage.py loaddata backup/custom/talents.xml
python3 manage.py loaddata backup/custom/blessingcurses.xml
python3 manage.py loaddata backup/custom/beneficeafflictions.xml




python3 manage.py loaddata backup/custom/configs.xml

echo "...done"
