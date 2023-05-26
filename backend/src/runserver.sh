#! /bin/sh

echo "### gunicorn running ###"
gunicorn --log-level debug main:app --reload 