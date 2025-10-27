#!/bin/sh
set -e  # exit on error

echo "Waiting for Postgres to be ready..."
until pg_isready -h db -p 5432; do
  echo "Waiting for Postgres..."
  sleep 1
done

echo "Postgres is ready! Running migrations..."
alembic upgrade head

echo "Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload