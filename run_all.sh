#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 data_generator/generate_data.py

echo "Starting the dashboard..."
streamlit run analysis/app.py
