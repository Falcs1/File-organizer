@echo off
echo.
echo ====================================
echo   Advanced File Organizer
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if file_organizer.py exists
if not exist "file_organizer.py" (
    echo ERROR: file_organizer.py not found!
    echo Make sure all files are in the same directory.
    echo.
    pause
    exit /b 1
)

REM Try to run the launcher first
if exist "run_organizer.py" (
    echo Starting File Organizer Launcher...
    python run_organizer.py
) else (
    echo Launcher not found, starting main application...
    python file_organizer.py
)

echo.
echo File Organizer finished.
pause 