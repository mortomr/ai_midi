# ai_mido MIDI Generator

An automated MIDI generation engine for producing structured musical data tailored for **pop/punk** and **singer-songwriter** styles.

## Overview

This project generates batches of musical patterns and exports them as MIDI files using Python and the `mido` library. Perfect for:

- Music producers looking for inspiration
- Backing track creation
- Learning music theory concepts
- MIDI pack development
- DAW project starters

## Musical Styles

### Pop/Punk
- Power chord progressions (I-V-vi-IV, etc.)
- Fast tempos (140-180 BPM)
- Driving drum patterns with eighth-note hi-hats
- Simple, energetic arpeggios
- Keys: G, C, D, E, A major

### Singer-Songwriter
- Complex chord voicings with 7ths and add9s
- Moderate tempos (70-120 BPM)
- Fingerpicking arpeggio patterns
- Subtle, acoustic-style drums
- Keys: Am, Em, Dm, C, G (major and minor)

## Project Structure

```
ai_midi/
├── data/
│   └── starter_dataset.json    # Master dataset (80 patterns)
├── src/
│   └── export_midi.py          # Python export script
├── generated/                  # Output MIDI files (created on export)
│   ├── chord_progressions/
│   ├── arpeggios/
│   ├── scales/
│   └── drum_patterns/
└── README.md
```

## Starter Dataset Contents

- **20 Chord Progressions**: Mix of pop/punk power chords and singer-songwriter progressions
- **20 Arpeggios**: Fingerpicking patterns and punk arpeggios
- **20 Scales**: Major, minor, pentatonic, blues, and modal scales
- **20 Drum Patterns**: From driving punk beats to subtle acoustic grooves

## Installation

### Requirements
- Python 3.x
- mido library

### Setup

```bash
# Install mido
pip install mido

# Clone or download this repository
cd ai_midi
```

## Usage

### Export All Patterns to MIDI

```bash
python src/export_midi.py
```

This will:
1. Read `data/starter_dataset.json`
2. Create the `generated/` directory structure
3. Export all 80 patterns as individual MIDI files
4. Organize files by type (chords, arpeggios, scales, drums)

### Output Example

```
generated/
├── chord_progressions/
│   ├── 01_G_major_pop_punk.mid
│   ├── 02_C_major_pop_punk.mid
│   ├── 06_A_minor_singer_songwriter.mid
│   └── ...
├── arpeggios/
│   ├── 01_G_major_singer_songwriter.mid
│   ├── 07_G_major_pop_punk.mid
│   └── ...
├── scales/
│   ├── 01_C_major.mid
│   ├── 02_A_minor.mid
│   └── ...
└── drum_patterns/
    ├── 01_pop_punk_160bpm.mid
    ├── 06_singer_songwriter_85bpm.mid
    └── ...
```

## Dataset Format

The JSON dataset uses a structured format for each pattern type:

### Chord Progression
```json
{
  "type": "chord_progression",
  "key": "G major",
  "tempo": 160,
  "complexity": 1,
  "style": "pop_punk",
  "pattern": [
    ["G5", [55, 62], 4],
    ["D5", [50, 57], 4]
  ],
  "description": "Classic power chord progression"
}
```

### Arpeggio
```json
{
  "type": "arpeggio",
  "key": "G major",
  "tempo": 120,
  "complexity": 2,
  "style": "singer_songwriter",
  "pattern": [
    [55, 0.5],
    [59, 0.5],
    [62, 0.5]
  ],
  "description": "Fingerpicking pattern"
}
```

### Scale
```json
{
  "type": "scale",
  "key": "C major",
  "tempo": 120,
  "complexity": 1,
  "style": "universal",
  "pattern": [
    [60, 0.5],
    [62, 0.5],
    [64, 0.5]
  ],
  "description": "C major scale"
}
```

### Drum Pattern
```json
{
  "type": "drum_pattern",
  "tempo": 160,
  "complexity": 1,
  "style": "pop_punk",
  "pattern": [
    {"drum": "kick", "note": 36, "hits": [0, 2]},
    {"drum": "snare", "note": 38, "hits": [1, 3]}
  ],
  "bars": 1,
  "description": "Basic punk beat"
}
```

## MIDI Note Reference

### Drum Mapping (General MIDI)
- **Kick**: 36
- **Snare**: 38
- **Rim shot**: 37
- **Closed Hi-hat**: 42
- **Open Hi-hat**: 46
- **Pedal Hi-hat**: 44
- **Ride**: 51
- **Crash**: 49
- **Low Tom**: 45
- **Tambourine**: 54
- **Shaker**: 70

### Piano Notes
- Middle C (C4): 60
- A4 (concert pitch): 69

## Customization

### Adding New Patterns

Edit `data/starter_dataset.json` and add new entries to the appropriate array:
- `chord_progressions`
- `arpeggios`
- `scales`
- `drum_patterns`

### Creating Custom Packs

You can create focused packs by:
1. Creating a new JSON file (e.g., `data/punk_only.json`)
2. Copying relevant patterns from the starter dataset
3. Modifying the export script to point to your custom file

### Adjusting Export Settings

In `src/export_midi.py`, you can modify:
- `ticks_per_beat`: MIDI resolution (default: 480)
- Velocity values for different instruments
- Output directory structure

## Complexity Ratings

Patterns are rated 1-5 for complexity:
- **1**: Simple, beginner-friendly
- **2**: Easy intermediate
- **3**: Intermediate
- **4**: Advanced
- **5**: Complex/experimental

## Tips for DAW Import

- **Tempo**: Each MIDI file has tempo embedded as metadata
- **Drum Channel**: Drums are on MIDI channel 10 (standard GM)
- **Velocity**:
  - Chords: 100
  - Arpeggios: 90
  - Scales: 85
  - Drums: 100
- **Format**: Type 1 MIDI files (multi-track)

## Future Expansions

Potential additions:
- Melodic fragments and hooks
- Basslines (root note patterns and walking bass)
- Rhythm grids (syncopation templates)
- Call-and-response patterns
- Bridge and pre-chorus transitions
- Genre-specific packs (emo, indie, folk-pop)

## License

This project generates musical patterns for creative use. Feel free to use the generated MIDI files in your own projects.

## Credits

Generated using Python + mido library
Patterns designed for pop/punk and singer-songwriter styles
