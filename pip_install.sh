#!/usr/bin/env bash
set -e  # exit immediately if any command fails

source .venv/bin/activate

echo "Installing engine..."
cd engine
pip install -e .

echo "Installing game..."
cd ../game
pip install -e .

echo "Done!"