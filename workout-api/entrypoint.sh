#!/bin/bash
set -e

source /app/.venv/bin/activate

alembic upgrade head

pip install python-multipart

exec uvicorn app:app --host 0.0.0.0 --port 8000