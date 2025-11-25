#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install mariadb
pip install flask

python3 app.py
