@echo off
REM Check if Python 3 is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python 3 is not installed. Please install it first.
    exit /b 1
)

REM Check if required packages are installed
python -c "import requests, inquirer, colorama" 2>nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install requests inquirer colorama
)

REM Run the script
python src/main.py 