#!/bin/bash

echo "Waiting for the database to be ready..."

# Use netcat (nc) to wait for the database to become available
until nc -z -v -w30 db 5432; do
  echo "Waiting for Postgres at db:5432..."
  sleep 1
done

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000