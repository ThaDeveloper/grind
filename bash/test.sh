#!/bin/sh
# test entry point
python manage.py migrate

coverage run --source=api -m pytest -v --no-cov && coverage report

exec $@
