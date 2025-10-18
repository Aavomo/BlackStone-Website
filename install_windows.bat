@echo off
echo Blackstone EG Partners - Flask Setup for Windows
echo ================================================

echo Checking Python version...
python --version

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing Flask (Method 1 - Simple)...
python -m pip install Flask Werkzeug Jinja2

if %errorlevel% neq 0 (
    echo.
    echo Method 1 failed, trying with trusted hosts...
    python -m pip install Flask Werkzeug Jinja2 --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
)

if %errorlevel% neq 0 (
    echo.
    echo Method 2 failed, trying user install...
    python -m pip install Flask Werkzeug Jinja2 --user
)

echo.
echo Testing Flask installation...
python -c "import flask; print('Flask version:', flask.__version__)"

if %errorlevel% eq 0 (
    echo.
    echo ✅ Flask installed successfully!
    echo.
    echo To run the website:
    echo   python app.py
    echo.
    echo Then open: http://localhost:5000
) else (
    echo.
    echo ❌ Flask installation failed
    echo Try running setup.py: python setup.py
)

pause
