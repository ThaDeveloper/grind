#!/bin/sh

if [ $DB_NAME = "grind" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "====> running migrations"
python manage.py migrate
echo "====> collecting static files"
python manage.py collectstatic --no-input --clear

exec $@
