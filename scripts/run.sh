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

#python manage.py shell < scripts/update_lores.py

#echo "Starting Celery..."
#kill -9 $(cat celeryd.pid)
#rm -f celeryd.pid
#celery worker -A dramatis_personae -l WARNING -B -E --detach --pidfile='celeryd.pid'

echo "Launching server..."
    python manage.py runserver 0.0.0.0:8088
