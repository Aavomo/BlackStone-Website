#!/usr/bin/env python3
"""
Setup script for Blackstone EG & Partners Flask Website
Handles installation and troubleshooting for different environments
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    return True

def install_packages(requirements_file="requirements_simple.txt"):
    """Try different installation methods"""
    methods = [
        # Method 1: Standard pip
        [sys.executable, "-m", "pip", "install", "-r", requirements_file],
        
        # Method 2: Upgrade pip first
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        
        # Method 3: Use trusted hosts
        [sys.executable, "-m", "pip", "install", "-r", requirements_file, 
         "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org", 
         "--trusted-host", "files.pythonhosted.org"],
        
        # Method 4: Individual packages
        [sys.executable, "-m", "pip", "install", "Flask"]
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"\n🔄 Trying installation method {i}...")
        try:
            result = subprocess.run(method, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print(f"✅ Installation successful with method {i}")
                return True
            else:
                print(f"❌ Method {i} failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"⏰ Method {i} timed out")
        except Exception as e:
            print(f"❌ Method {i} error: {e}")
    
    return False

def test_flask_import():
    """Test if Flask can be imported"""
    try:
        import flask
        print(f"✅ Flask imported successfully (version: {flask.__version__})")
        return True
    except ImportError:
        print("❌ Flask import failed")
        return False

def create_simple_app():
    """Create a minimal Flask app for testing"""
    app_content = '''from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Flask is working!</h1><p>Blackstone EG & Partners website ready.</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open("test_app.py", "w") as f:
        f.write(app_content)
    print("📝 Created test_app.py")

def main():
    print("🚀 Blackstone EG & Partners - Flask Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Try to install packages
    print("\n📦 Installing Flask and dependencies...")
    if install_packages():
        # Test Flask import
        if test_flask_import():
            print("\n✅ Setup completed successfully!")
            create_simple_app()
            print("\n🌐 Run 'python test_app.py' to test Flask")
            print("🌐 Then run 'python app.py' for the full website")
        else:
            print("\n❌ Flask installation verification failed")
    else:
        print("\n❌ All installation methods failed")
        print("\n🔧 Manual solutions:")
        print("1. Check your internet connection")
        print("2. Try: python -m pip install --upgrade pip")
        print("3. Try: python -m pip install Flask --user")
        print("4. Use conda: conda install flask")
        print("5. Download wheels manually from pypi.org")

if __name__ == "__main__":
    main()
