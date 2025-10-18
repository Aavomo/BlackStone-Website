# Blackstone EG & Partners - Flask Website

## 🚨 **Quick Fix for Installation Issues**

### **Problem:** Network connectivity issues with pip

### **Solutions (try in order):**

#### **For Windows:**
```cmd
# Run the automated installer
install_windows.bat

# OR manually:
python -m pip install --upgrade pip
python -m pip install Flask --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

#### **For Linux/Mac:**
```bash
# Run the automated installer
bash install_linux.sh

# OR manually:
python3 -m pip install --upgrade pip
python3 -m pip install Flask
```

#### **Alternative Methods:**

1. **Use the setup script:**
   ```bash
   python setup.py
   ```

2. **Install without version constraints:**
   ```bash
   pip install -r requirements_simple.txt
   ```

3. **Use conda instead:**
   ```bash
   conda install flask
   ```

4. **Install from wheel files:**
   - Download Flask wheel from https://pypi.org/project/Flask/#files
   - Install locally: `pip install Flask-3.0.0-py3-none-any.whl`

## 🚀 **Running the Website**

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open browser:** http://localhost:5000

## 🔧 **Troubleshooting**

### **Network Issues:**
- Check firewall settings
- Try mobile hotspot
- Use `--trusted-host` flags
- Install packages individually

### **Python 3.13.2 Compatibility:**
This website is compatible with Python 3.8+ including 3.13.2

### **Permission Issues:**
```bash
# Windows (Run as Administrator)
pip install Flask --user

# Linux/Mac
sudo pip install Flask
# OR
pip install Flask --user
```

## 📁 **Project Structure**
```
.
├── app.py                 # Main Flask application
├── requirements_simple.txt # Simple dependencies
├── setup.py              # Automated setup script
├── install_windows.bat   # Windows installer
├── install_linux.sh      # Linux/Mac installer
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── services.html
    ├── team.html
    ├── about.html
    ├── contact.html
    └── 404.html
```

## 🌐 **Features**

- ✅ **Python 3.8+ Compatible** (including 3.13.2)
- ✅ **Network-resilient installation**
- ✅ **Multiple installation methods**
- ✅ **Cross-platform support** (Windows/Linux/Mac)
- ✅ **Professional business website**
- ✅ **Responsive design**
- ✅ **Contact form with validation**

## 📞 **Still Having Issues?**

Try the minimal test first:
```python
# test_flask.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Flask Works!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
```

Run: `python test_flask.py`
