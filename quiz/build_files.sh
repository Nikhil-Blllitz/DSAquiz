#!/bin/bash

echo "BUILD START"

# Collect static files from multiple folders
python manage.py collectstatic --noinput

# Install required packages
python3.9 -m pip install -r requirements.txt

# Collect static files again (the clear option is usually not needed unless you want to delete old static files)
python manage.py collectstatic --noinput --clear

echo "BUILD END"
