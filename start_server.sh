#!/bin/bash
echo "Starting AI Lung Cancer Detection Server..."
echo ""
cd backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
