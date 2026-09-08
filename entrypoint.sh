#!/bin/sh
set -e

# Apply database migrations
if [ "$DJANGO_SKIP_MIGRATIONS" != "1" ]; then
  python manage.py migrate --noinput
fi

# Collect static files
if [ "$DJANGO_SKIP_COLLECTSTATIC" != "1" ]; then
  python manage.py collectstatic --noinput || true
fi

exec python manage.py runserver 0.0.0.0:8000
