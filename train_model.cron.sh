#!/bin/bash

echo "Début du réentraînement du modèle..."
source ./.venv/bin/activate  # Active l'environnement virtuel pour linux (à adapter pour Windows)
python ./train_model.py
echo "✅ Réentraînement terminé."
