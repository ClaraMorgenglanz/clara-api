#!/bin/bash
cd "$(dirname "$0")"
uvicorn clara_api_service:app --reload --host 0.0.0.0 --port 8000
