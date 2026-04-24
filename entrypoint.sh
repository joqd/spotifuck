#!/bin/bash
set -e

echo "🚀 Running migrations..."
uv run python manage.py migrate

echo "🚀 Starting Celery worker & beat..."
uv run celery -A spotifuck worker -l info --max-tasks-per-child=100 &
uv run celery -A spotifuck beat -l info &

echo "🚀 Starting Django bot..."
uv run python manage.py runbot