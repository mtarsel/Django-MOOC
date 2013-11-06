#!/bin/bash

rm -rf mooc_database.db
python manage.py syncdb
python manage.py runserver
