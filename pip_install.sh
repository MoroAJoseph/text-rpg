#!/usr/bin/env bash
set -e

# 1. Activate environment
source .venv/bin/activate

# 2. Determine installation mode
MODE=$1
EXTRAS=""

case $MODE in
    test)
        EXTRAS="[test]"
        echo "🔧 Mode: Testing (pytest + benchmarks)"
        ;;
    dev)
        EXTRAS="[dev]"
        echo "🛠️ Mode: Development (pydantic + linting)"
        ;;
    all)
        EXTRAS="[dev,test]"
        echo "🚀 Mode: Full Environment (dev + test)"
        ;;
    *)
        echo "📦 Mode: Standard (core only)"
        ;;
esac

# 3. Install Engine
echo "Installing engine..."
pip install -e "./engine${EXTRAS}"

# 4. Install Game (assuming it also has a pyproject.toml)
echo "Installing game..."
pip install -e "./game"

echo "✅ Done!"