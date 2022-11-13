# ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤ 
# ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘

#!/bin/bash
    clear
    export DJANGO_SETTINGS_MODULE=dramatis_personae.settings.local

echo "Make migrations..."
    python manage.py makemigrations
echo "Migrate..."
    python manage.py migrate
echo "Collecting statics"
    python manage.py collectstatic --noinput --clear --link -v 0
echo "Launching tests..."
    python manage.py test --failfast --parallel 4 -v 0
echo "...done."