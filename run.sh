#!/bin/sh


#定时获取
python3 /app/static/time_access_token.py &&
python3 /app/manage.py runserver 0.0.0.0:80
