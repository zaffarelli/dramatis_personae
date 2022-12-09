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

    python --version

echo "Launching standard dev server..."
   python manage.py runserver -v 3 0.0.0.0:8088

#echo "Launching Daphne server..."
#    daphne -b 0.0.0.0 -p 8088 dramatis_personae.asgi:application

#echo "Launching Hypercorn server..."
#    hypercorn 0.0.0.0:8088 dramatis_personae.asgi:application