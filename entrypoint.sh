#!/bin/bash

# Attendre que la base de données soit prête
echo "Waiting for MySQL to start..."
while ! nc -z db 3306; do
  sleep 1
done

echo "MySQL started"

# Appliquer les migrations de la base de données
flask db upgrade

# Lancer l'application Flask
flask run --host=0.0.0.0