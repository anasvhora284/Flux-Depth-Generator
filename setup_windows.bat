@echo off
setlocal enabledelayedexpansion

REM Change to script directory
cd /d %~dp0

echo === Creating virtual environment (.venv) ===
python -m venv .venv
if errorlevel 1 (
    echo Failed to create virtual environment. Ensure Python is in PATH.
    pause
    exit /b 1
)

echo === Activating virtual environment ===
call .venv\Scripts\activate

echo === Upgrading pip ===
python -m pip install --upgrade pip

echo === Installing requirements ===
pip install -r requirements.txt

echo === Launching Streamlit app ===
streamlit run app.py

endlocal
