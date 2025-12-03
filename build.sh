#!/usr/bin/env bash
set -o errexit

# Navigate to the Django project directory
cd src

# Install Python dependencies from requirements.txt
pip install -r ../requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Apply database migrations for Neon PostgreSQL
python manage.py migrate