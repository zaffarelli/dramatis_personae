# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear

echo "Loading reference data..."
python3 manage.py loaddata backup/weaponrefs.xml
python3 manage.py loaddata backup/skillrefs.xml
python3 manage.py loaddata backup/armorrefs.xml
python3 manage.py loaddata backup/shieldrefs.xml
python3 manage.py loaddata backup/beneficeafflictionrefs.xml
python3 manage.py loaddata backup/castroles.xml
python3 manage.py loaddata backup/castprofiles.xml
python3 manage.py loaddata backup/casteverymans.xml

python3 manage.py loaddata backup/blank_epics.xml
python3 manage.py loaddata backup/blank_configs.xml

echo "...done"
