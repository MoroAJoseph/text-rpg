#!/bin/bash
set -e

# --- Activate virtualenv ---
source .venv/bin/activate

# --- Configuration ---
MAIN_MODULE="main.py"
DIST_DIR="dist"
BUILD_DIR="build"
EXE_NAME="text-rpg"

echo "Cleaning previous builds..."
rm -rf $DIST_DIR $BUILD_DIR __pycache__ *.spec

echo "Building executable with PyInstaller..."
pyinstaller \
    --name $EXE_NAME \
    --onefile \
    --console \
    $MAIN_MODULE

echo "Build complete!"
echo "Executable is at: $DIST_DIR/$EXE_NAME"