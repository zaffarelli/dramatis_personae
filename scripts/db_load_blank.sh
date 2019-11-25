# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash

echo "Loading reference data..."
scripts/db_load_initial.sh
echo -e "\e[0;35m...done\e[0;m"

echo "Loading user data..."
python3 manage.py loaddata backup/custom/epic.xml
python3 manage.py loaddata backup/reference/blank_epic.xml
python3 manage.py loaddata backup/reference/blank_config.xml
echo -e "\e[0;35m...done\e[0;m"
