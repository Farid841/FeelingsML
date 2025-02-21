#!/bin/sh

echo "Waiting for MySQL..."
while ! nc -z db 3306; do
  sleep 1
done
echo "MySQL started"

flask db upgrade

flask run --host=0.0.0.0