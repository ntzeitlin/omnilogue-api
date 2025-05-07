#!/bin/bash

rm db.sqlite3
rm -rf ./omnilogueapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations omnilogueapi
python3 manage.py migrate omnilogueapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata userprofiles
python3 manage.py loaddata categories
python3 manage.py loaddata tags
python3 manage.py loaddata stories
python3 manage.py loaddata story_tags
python3 manage.py loaddata story_sections
python3 manage.py loaddata story_links
python3 manage.py loaddata bookshelves
python3 manage.py loaddata reviews
python3 manage.py loaddata story_reading_histories
python3 manage.py loaddata bookshelf_stories
python3 manage.py process_stories
