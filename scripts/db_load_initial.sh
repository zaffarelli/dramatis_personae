# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

python3 manage.py flush

echo "Loading reference data..."
python3 manage.py loaddata backup/reference/weaponrefs.xml
python3 manage.py loaddata backup/reference/skillrefs.xml
python3 manage.py loaddata backup/reference/armorrefs.xml
python3 manage.py loaddata backup/reference/shieldrefs.xml
python3 manage.py loaddata backup/reference/talentrefs.xml
python3 manage.py loaddata backup/reference/beneficeafflictionrefs.xml
python3 manage.py loaddata backup/reference/roles.xml
python3 manage.py loaddata backup/reference/profiles.xml
python3 manage.py loaddata backup/reference/species.xml

python3 manage.py loaddata backup/reference/blank_epics.xml
python3 manage.py loaddata backup/reference/blank_configs.xml

echo "...done"
