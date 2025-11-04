#!/bin/bash

echo "setting up website"

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip

pip install flask
pip install mariadb

python3 app.py

