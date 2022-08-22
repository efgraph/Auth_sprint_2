#!/bin/bash
./wait-for-it.sh db:5432 -t 15 -- echo "postgres is up"
./wait-for-it.sh storage:6379 -t 15 -- echo "storage is up"
cd src
flask db init
flask db mirgate
flask db upgrade
python3 create_superuser.py
python3 -m pytest -v -s
python3 pywsgi.py
