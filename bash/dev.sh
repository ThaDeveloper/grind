#!/bin/sh
# dev entry point
#clears out the database
python manage.py flush --no-input
python manage.py migrate

# python manage.py collectstatic --no-input --clear
exec $@
