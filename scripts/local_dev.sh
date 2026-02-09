#!/bin/bash
# Local development helper script

echo "Starting local environment..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
