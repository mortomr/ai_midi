"""
Web interface for AI MIDI Drum Generator
Flask application with simple, intuitive UI
"""

from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path
import tempfile
import os
from datetime import datetime

from generators.drum_generator import DrumPatternGenerator
from export_midi import export_drum_pattern

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# Store generated files temporarily - use absolute path
# Get the project root directory (parent of src)
PROJECT_ROOT = Path(__file__).parent.parent
TEMP_DIR = PROJECT_ROOT / 'generated' / 'web_temp'
TEMP_DIR.mkdir(parents=True, exist_ok=True)


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_pattern():
    """Generate drum pattern based on parameters from web UI"""
    try:
        # Parse parameters from request
        data = request.json

        tempo = int(data.get('tempo', 140))
        style = data.get('style', 'pop_punk')
        section = data.get('section') if data.get('section') != 'none' else None
        bars = int(data.get('bars', 4))
        density = float(data.get('density', 0.7))
        variation = float(data.get('variation', 0.5))
        syncopation = float(data.get('syncopation', 0.3))
        fill_frequency = float(data.get('fill_frequency', 0.25))
        kick_pattern = data.get('kick_pattern', 'punk')
        hihat_pattern = data.get('hihat_pattern', 'eighth')
        seed = data.get('seed')  # Optional - None if not provided

        # Generate pattern
        generator = DrumPatternGenerator(tempo=tempo, seed=seed)
        pattern = generator.generate_pattern(
            style=style,
            bars=bars,
            density=density,
            variation=variation,
            syncopation=syncopation,
            fill_frequency=fill_frequency,
            kick_pattern=kick_pattern,
            hihat_pattern=hihat_pattern,
            section=section
        )

        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"drum_pattern_{timestamp}.mid"
        output_path = TEMP_DIR / filename

        # Export to MIDI
        export_drum_pattern(pattern, str(output_path))

        return jsonify({
            'success': True,
            'filename': filename,
            'description': pattern['description'],
            'download_url': f'/api/download/{filename}'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated MIDI file"""
    file_path = TEMP_DIR / filename
    if file_path.exists():
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='audio/midi'
        )
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/api/info')
def get_info():
    """Get available options for dropdowns"""
    return jsonify({
        'styles': ['pop_punk', 'singer_songwriter', 'reggae_ska', 'metal', 'jazz', 'rock', 'indie', 'electronic', 'hybrid'],
        'sections': ['none', 'intro', 'verse', 'pre_chorus', 'chorus', 'bridge', 'breakdown', 'outro'],
        'kick_patterns': ['punk', 'four_floor', 'half_time', 'double', 'skank', 'one_drop', 'd_beat'],
        'hihat_patterns': ['eighth', 'sixteenth', 'ride', 'open_closed', 'skank', 'swing']
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🥁 AI MIDI Drum Generator - Web Interface")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
