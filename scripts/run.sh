# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
#!/bin/bash
    clear
    export DJANGO_SETTINGS_MODULE=dramatis_personae.settings.local
echo "Make migrations..."
    python3 manage.py makemigrations
echo "Migrate..."
    python3 manage.py migrate
echo "Collecting statics"
    python3 manage.py collectstatic --noinput --clear --link -v 0

python manage.py shell < scripts/update_alliances.py

echo "Launching server..."
    python3 manage.py runserver 0.0.0.0:8088
