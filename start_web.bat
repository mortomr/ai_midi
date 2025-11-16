@echo off
REM Start the AI MIDI Drum Generator Web Interface

cd /d "%~dp0"

echo.
echo ============================================================
echo 🥁 AI MIDI Drum Generator - Web Interface
echo ============================================================
echo.
echo Starting server...
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

.venv\Scripts\python.exe src\web_app.py

pause
