#!/bin/bash
export FLASK_APP=./src/main.py
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate
flask run -h 127.0.0.1
