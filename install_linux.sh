#!/bin/bash

# Blackstone EG Partners - Flask Setup for Linux/Mac
echo "🚀 Blackstone EG Partners - Flask Setup"
echo "======================================"

echo "🐍 Checking Python version..."
python3 --version

echo ""
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

echo ""
echo "🔧 Installing Flask..."
python3 -m pip install Flask Werkzeug Jinja2

if [ $? -ne 0 ]; then
    echo "Method 1 failed, trying with user install..."
    python3 -m pip install Flask Werkzeug Jinja2 --user
fi

echo ""
echo "🧪 Testing Flask installation..."
python3 -c "import flask; print('Flask version:', flask.__version__)"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Flask installed successfully!"
    echo ""
    echo "To run the website:"
    echo "  python3 app.py"
    echo ""
    echo "Then open: http://localhost:5000"
else
    echo ""
    echo "❌ Flask installation failed"
    echo "Try running: python3 setup.py"
fi
