#!/usr/bin/env bash

echo "🚀 Starting CrewAI Environment Repair..."

# 1. Ensure we are in the virtual environment
if [ -d ".venv" ]; then
    echo "✅ Found virtual environment. Activating..."
    source .venv/Scripts/activate
else
    echo "❌ .venv not found! Creating one now..."
    python -m venv .venv
    source .venv/Scripts/activate
fi

# 2. Clean up broken packages
echo "🧹 Cleaning up old onnxruntime and cache..."
pip uninstall onnxruntime onnxruntime-gpu -y
pip cache purge

# 3. Force install stable versions
# We use 1.16.3 because it is the most stable for Python 3.11 on Windows
echo "📦 Installing stable dependencies..."
pip install --upgrade pip
pip install onnxruntime==1.16.3
pip install crewai langchain-groq

# 4. Verify installation
echo "🔍 Verifying ONNX installation..."
python -c "import onnxruntime; print('✅ ONNX Version:', onnxruntime.get_device())" || echo "⚠️ ONNX still has issues, but may work if memory=False."

echo "------------------------------------------------"
echo "✨ Setup Complete! Always run your app with:"
echo "streamlit run app.py"
echo "------------------------------------------------"