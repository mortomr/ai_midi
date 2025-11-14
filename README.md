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
│   ├── starter_dataset.json    # Master dataset (80 patterns)
│   └── rudiments_dataset.json  # PAS drum rudiments (32 patterns)
├── src/
│   ├── generators/             # Generative engines
│   │   └── drum_generator.py   # Drum pattern generator
│   ├── export_midi.py          # MIDI export utilities
│   ├── export_rudiments.py     # Rudiments export script
│   └── generate_drums.py       # CLI drum generator
├── examples/
│   └── drum_generator_demo.sh  # Demo script
├── generated/                  # Output MIDI files (created on export)
│   ├── chord_progressions/
│   ├── arpeggios/
│   ├── scales/
│   ├── drum_patterns/
│   ├── rudiments/
│   └── generated_drums/        # Generatively created patterns
└── README.md
```

## Starter Dataset Contents

- **20 Chord Progressions**: Mix of pop/punk power chords and singer-songwriter progressions
- **20 Arpeggios**: Fingerpicking patterns and punk arpeggios
- **20 Scales**: Major, minor, pentatonic, blues, and modal scales
- **20 Drum Patterns**: From driving punk beats to subtle acoustic grooves

## Drum Rudiments Collection (NEW!)

- **32 PAS International Drum Rudiments**: Professional drum patterns based on the Percussive Arts Society's 40 International Drum Rudiments
  - **Roll Rudiments**: Single stroke, double stroke, five/six/seven/nine/thirteen/seventeen stroke rolls, triple stroke roll
  - **Diddle Rudiments**: Single/double/triple paradiddle, paradiddle-diddle
  - **Flam Rudiments**: Flam, flam accent, flam tap, flamacue, flam paradiddle, Swiss Army triplet, pataflafla
  - **Drag Rudiments**: Drag (ruff), single/double drag tap, lesson 25, single/double ratamacue

### Rudiment Features:
- **Multiple Orchestrations**: snare-only, snare+bass, full kit descending, toms, hi-hat+snare, ride patterns
- **Musical Usage**: fills, accents, rhythms, transitions
- **Style Adaptations**: Pop/punk (fast, aggressive), singer-songwriter (subtle, dynamic)
- **Grace Notes**: Authentic flams and drags with proper grace note notation
- **Dynamic Velocities**: Accent patterns with varied velocities for realism
- **Hand Sticking**: R/L notation included in metadata for learning

## Generative Drum Engine (NEW!)

**The game changer!** Instead of playing back static patterns, the drum generator creates unique patterns based on musical rules and your parameters.

### How It's Different
- **Static Datasets**: Translator - plays back pre-written patterns
- **Generative Engine**: Creator - follows music theory rules to make infinite variations

### Controllable Parameters

Turn these knobs to shape your drum patterns:

- **tempo**: BPM (72-200+)
- **style**: pop_punk, singer_songwriter, hybrid
- **bars**: Length (1-64+)
- **density**: 0.0-1.0 (sparse to busy)
- **variation**: 0.0-1.0 (repetitive to dynamic)
- **syncopation**: 0.0-1.0 (straight to off-beat)
- **fill_frequency**: 0.0-1.0 (how often fills occur)
- **kick_pattern**: punk, four_floor, half_time, double
- **hihat_pattern**: eighth, sixteenth, ride, open_closed

### Example Usage

```bash
# Fast punk beat
python src/generate_drums.py --tempo 165 --style pop_punk --density 0.8

# Mellow singer-songwriter
python src/generate_drums.py --tempo 85 --style singer_songwriter --variation 0.3

# Four-on-the-floor with sixteenth hats
python src/generate_drums.py --kick four_floor --hihat sixteenth --bars 16

# Generate 10 variations of same style
python src/generate_drums.py --count 10 --style pop_punk --seed 42
```

### Under the Hood

The generator uses:
- **Music Theory Rules**: Backbeat always on 2 & 4, fills on phrase endings
- **Style Templates**: Different rules for punk vs. singer-songwriter
- **Controlled Randomization**: Parameters guide variation within musical constraints
- **Rudiment Integration**: Fills use rudiment-inspired patterns

**Every generation is unique** - same parameters create similar but not identical patterns.

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
# Export starter dataset (chords, arpeggios, scales, drum patterns)
python src/export_midi.py

# Export drum rudiments
python src/export_rudiments.py
```

**Starter Dataset** export will:
1. Read `data/starter_dataset.json`
2. Create the `generated/` directory structure
3. Export all 80 patterns as individual MIDI files
4. Organize files by type (chords, arpeggios, scales, drums)

**Rudiments** export will:
1. Read `data/rudiments_dataset.json`
2. Export all 32 rudiment patterns as individual MIDI files
3. Organize by category (roll, diddle, flam, drag) and orchestration
4. Include proper grace notes for flams and drags

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
├── drum_patterns/
│   ├── 01_pop_punk_160bpm.mid
│   ├── 06_singer_songwriter_85bpm.mid
│   └── ...
└── rudiments/
    ├── 01_roll_Single_Stroke_Roll_snare_only_fill.mid
    ├── 06_diddle_Single_Paradiddle_snare_only_rhythm.mid
    ├── 10_flam_Flam_snare_only_accent.mid
    ├── 14_drag_Drag_(Ruff)_snare_only_accent.mid
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

### Rudiment Pattern
```json
{
  "type": "rudiment",
  "category": "diddle",
  "name": "Single Paradiddle",
  "sticking": "RLRR-LRLL",
  "tempo": 155,
  "complexity": 2,
  "style": "pop_punk",
  "orchestration": "snare_only",
  "usage": "rhythm",
  "pattern": [
    {"hand": "R", "note": 38, "time": 0, "duration": 0.125, "velocity": 95},
    {"hand": "L", "note": 38, "time": 0.125, "duration": 0.125, "velocity": 85},
    {"hand": "R", "note": 38, "time": 0.25, "duration": 0.125, "velocity": 95}
  ],
  "bars": 0.5,
  "description": "Classic paradiddle pattern"
}
```

**Rudiment fields:**
- `category`: roll, diddle, flam, drag
- `sticking`: R/L hand pattern notation
- `orchestration`: snare_only, full_kit_descending, snare_bass, hihat_snare, etc.
- `usage`: fill, accent, rhythm, transition
- `grace`: Set to `true` for grace notes (flams/drags)
- Each note has precise `time`, `duration`, and `velocity`

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

Or edit `data/rudiments_dataset.json` to add new rudiments to:
- `rudiment_patterns`

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
- **Drum Channel**: Drums and rudiments are on MIDI channel 10 (standard GM)
- **Velocity**:
  - Chords: 100
  - Arpeggios: 90
  - Scales: 85
  - Drums: 100
  - Rudiments: 60-110 (dynamic, with accents and grace notes)
- **Format**: Type 1 MIDI files (multi-track)
- **Grace Notes**: Rudiments with flams/drags have grace notes (very short durations, 0.03 beats)

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
Drum rudiments based on the PAS (Percussive Arts Society) 40 International Drum Rudiments
