#!/usr/bin/env bash
# 오류 발생 시 즉시 중단
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate