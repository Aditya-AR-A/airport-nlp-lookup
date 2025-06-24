@echo off
setlocal enabledelayedexpansion

echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ">>> Python not found in PATH."
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version') do set PY_VER=%%v
for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo ">>> Python version must be 3.8 or higher."
    pause
    exit /b 1
) else if %MAJOR%==3 if %MINOR% LSS 8 (
    echo ">>> Python version must be 3.8 or higher."
    pause
    exit /b 1
)

echo ">>> Python version is %MAJOR%.%MINOR% — OK."

:: Check if 'env' directory exists
if exist env (
    echo ">>> Virtual environment already exists."
) else (
    echo "🛠️ Creating virtual environment..."
    python -m venv env
    if errorlevel 1 (
        echo ">>> Failed to create virtual environment."
        pause
        exit /b 1
    )
    echo ">>> Virtual environment created successfully."
)

:: Use virtualenv's Python
set PY=env\Scripts\python.exe

echo "🔄 Upgrading pip safely..."
%PY% -m pip install --upgrade pip
if errorlevel 1 (
    echo ">>> Failed to upgrade pip."
    pause
    exit /b 1
)

echo ">>> Installing required packages from requirements.txt..."
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
    echo ">>> Failed to install required packages."
    pause
    exit /b 1
)

echo ">>> Environment setup completed successfully."
exit