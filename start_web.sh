#!/bin/bash
# Start the AI MIDI Drum Generator Web Interface

cd "$(dirname "$0")"

echo ""
echo "============================================================"
echo "🥁 AI MIDI Drum Generator - Web Interface"
echo "============================================================"
echo ""
echo "Starting server..."
echo ""
echo "Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python src/web_app.py
