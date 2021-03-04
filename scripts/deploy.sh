# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
clear
#echo "Updating Dramatis Personae..."
#cartograph/makedp.py
#echo "Cleaning PDF..."
#rm -f cartograph/pdf/*.pdf
echo "Make migrations..."
python3 manage.py makemigrations
echo "Migrate..."
python3 manage.py migrate
echo "Updating CSS from SCSS..."
sass ./collector/static/collector/styles.scss ./collector/static/collector/styles.css
echo "Collecting statics"
python3 manage.py collectstatic --noinput --clear --link -v 0
echo "Launching server..."
python3 manage.py runserver 0.0.0.0:8088
