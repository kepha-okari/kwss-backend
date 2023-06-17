#!/bin/bash

# makemigrations
python3 manage.py makemigrations

# migrate
python3 manage.py migrate
