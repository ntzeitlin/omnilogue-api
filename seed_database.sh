#!/bin/bash

rm db.sqlite3
rm -rf ./omnilogueapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations omnilogueapi
python3 manage.py migrate omnilogueapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

