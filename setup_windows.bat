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

echo === Checking for model weights ===
if not exist "Depth_Anything_V2\checkpoints" mkdir "Depth_Anything_V2\checkpoints"
if not exist "Depth_Anything_V2\checkpoints\depth_anything_v2_vits.pth" (
    echo === Downloading Depth-Anything-V2-Small model ===
    powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth?download=true' -OutFile 'Depth_Anything_V2\checkpoints\depth_anything_v2_vits.pth'"
)

echo === Launching Streamlit app ===
streamlit run app.py

endlocal
