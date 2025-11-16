// AI MIDI Drum Generator - Frontend JavaScript

// Update slider value displays
const sliders = [
    { id: 'tempo', display: 'tempo-value', unit: '' },
    { id: 'bars', display: 'bars-value', unit: '' },
    { id: 'density', display: 'density-value', unit: '', decimals: 2 },
    { id: 'variation', display: 'variation-value', unit: '', decimals: 2 },
    { id: 'syncopation', display: 'syncopation-value', unit: '', decimals: 2 },
    { id: 'fill_frequency', display: 'fill-value', unit: '', decimals: 2 }
];

sliders.forEach(slider => {
    const input = document.getElementById(slider.id);
    const display = document.getElementById(slider.display);

    input.addEventListener('input', (e) => {
        let value = e.target.value;
        if (slider.decimals !== undefined) {
            value = parseFloat(value).toFixed(slider.decimals);
        }
        display.textContent = value + slider.unit;
    });
});

// Preset configurations
const presets = {
    'fast-punk': {
        tempo: 165,
        style: 'pop_punk',
        section: 'chorus',
        bars: 8,
        density: 0.9,
        variation: 0.5,
        syncopation: 0.4,
        fill_frequency: 0.3,
        kick_pattern: 'punk',
        hihat_pattern: 'eighth'
    },
    'mellow': {
        tempo: 85,
        style: 'singer_songwriter',
        section: 'verse',
        bars: 8,
        density: 0.5,
        variation: 0.3,
        syncopation: 0.2,
        fill_frequency: 0.15,
        kick_pattern: 'half_time',
        hihat_pattern: 'ride'
    },
    'ska': {
        tempo: 140,
        style: 'reggae_ska',
        section: 'chorus',
        bars: 8,
        density: 0.8,
        variation: 0.5,
        syncopation: 0.3,
        fill_frequency: 0.25,
        kick_pattern: 'skank',
        hihat_pattern: 'skank'
    },
    'reggae': {
        tempo: 90,
        style: 'reggae_ska',
        section: 'verse',
        bars: 8,
        density: 0.7,
        variation: 0.4,
        syncopation: 0.3,
        fill_frequency: 0.2,
        kick_pattern: 'one_drop',
        hihat_pattern: 'skank'
    },
    'hardcore': {
        tempo: 180,
        style: 'pop_punk',
        section: 'chorus',
        bars: 4,
        density: 1.0,
        variation: 0.5,
        syncopation: 0.6,
        fill_frequency: 0.3,
        kick_pattern: 'd_beat',
        hihat_pattern: 'sixteenth'
    }
};

// Apply preset
document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const presetName = btn.dataset.preset;
        const preset = presets[presetName];

        if (preset) {
            Object.keys(preset).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    element.value = preset[key];

                    // Trigger input event to update displays
                    const event = new Event('input', { bubbles: true });
                    element.dispatchEvent(event);
                }
            });
        }
    });
});

// Generate pattern
const generateBtn = document.getElementById('generate-btn');
const statusDiv = document.getElementById('status');
const downloadSection = document.getElementById('download-section');
const downloadLink = document.getElementById('download-link');
const patternDescription = document.getElementById('pattern-description');

generateBtn.addEventListener('click', async () => {
    // Gather all parameters
    const params = {
        tempo: document.getElementById('tempo').value,
        style: document.getElementById('style').value,
        section: document.getElementById('section').value,
        bars: document.getElementById('bars').value,
        density: document.getElementById('density').value,
        variation: document.getElementById('variation').value,
        syncopation: document.getElementById('syncopation').value,
        fill_frequency: document.getElementById('fill_frequency').value,
        kick_pattern: document.getElementById('kick_pattern').value,
        hihat_pattern: document.getElementById('hihat_pattern').value
    };

    // Update UI
    generateBtn.disabled = true;
    generateBtn.textContent = '🎵 Generating...';
    statusDiv.textContent = 'Creating your drum pattern...';
    statusDiv.className = 'status loading';
    downloadSection.style.display = 'none';

    try {
        // Make API request
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        const result = await response.json();

        if (result.success) {
            // Success!
            statusDiv.textContent = '✅ Pattern generated successfully!';
            statusDiv.className = 'status success';

            patternDescription.textContent = result.description;
            downloadLink.href = result.download_url;
            downloadLink.download = result.filename;

            downloadSection.style.display = 'block';
        } else {
            // Error
            statusDiv.textContent = '❌ Error: ' + result.error;
            statusDiv.className = 'status error';
        }
    } catch (error) {
        statusDiv.textContent = '❌ Network error: ' + error.message;
        statusDiv.className = 'status error';
    } finally {
        // Re-enable button
        generateBtn.disabled = false;
        generateBtn.textContent = '🎵 Generate Drum Pattern';
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🥁 AI MIDI Drum Generator - Ready!');
});
