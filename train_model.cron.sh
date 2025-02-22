#!/bin/bash

echo "Starting model retraining..."

# Wait for database
while ! nc -z db 3306; do
  sleep 1
done

# Run training script
python /app/train_model.py

echo "✅ Retraining completed."