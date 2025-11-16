#!/usr/bin/env python3
"""
ai_mido MIDI Exporter
Exports structured musical patterns from JSON to MIDI files using mido
"""

import json
import os
from pathlib import Path
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo


def create_output_dir(base_path="generated"):
    """Create output directory structure"""
    dirs = [
        f"{base_path}/chord_progressions",
        f"{base_path}/arpeggios",
        f"{base_path}/scales",
        f"{base_path}/drum_patterns",
        f"{base_path}/rudiments"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    return base_path


def beats_to_ticks(beats, ticks_per_beat=480):
    """Convert beats to MIDI ticks"""
    return int(beats * ticks_per_beat)


def export_chord_progression(data, output_path, ticks_per_beat=480):
    """
    Export chord progression to MIDI file

    Pattern format: [chord_name, [notes], duration_in_beats]
    """
    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # Add tempo
    tempo = bpm2tempo(data['tempo'])
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Add track name
    track.append(MetaMessage('track_name', name=f"{data['key']} - {data['description']}", time=0))

    # Process chord progression
    for chord_name, notes, duration in data['pattern']:
        # Note on messages
        for i, note in enumerate(notes):
            track.append(Message('note_on', note=note, velocity=100, time=0))

        # Note off messages (after duration)
        for i, note in enumerate(notes):
            if i == 0:
                # First note off comes after the duration
                track.append(Message('note_off', note=note, velocity=0,
                                   time=beats_to_ticks(duration, ticks_per_beat)))
            else:
                # Subsequent note offs have no delay
                track.append(Message('note_off', note=note, velocity=0, time=0))

    mid.save(output_path)
    print(f"✓ Exported chord progression: {output_path}")


def export_arpeggio(data, output_path, ticks_per_beat=480):
    """
    Export arpeggio pattern to MIDI file

    Pattern format: [[note, duration_in_beats], ...]
    """
    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # Add tempo
    tempo = bpm2tempo(data['tempo'])
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Add track name
    track.append(MetaMessage('track_name', name=f"{data['key']} - {data['description']}", time=0))

    # Process arpeggio pattern
    for note, duration in data['pattern']:
        # Note on
        track.append(Message('note_on', note=note, velocity=90, time=0))
        # Note off after duration
        track.append(Message('note_off', note=note, velocity=0,
                           time=beats_to_ticks(duration, ticks_per_beat)))

    mid.save(output_path)
    print(f"✓ Exported arpeggio: {output_path}")


def export_scale(data, output_path, ticks_per_beat=480):
    """
    Export scale to MIDI file

    Pattern format: [[note, duration_in_beats], ...]
    """
    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # Add tempo
    tempo = bpm2tempo(data['tempo'])
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Add track name
    track.append(MetaMessage('track_name', name=f"{data['key']} - {data['description']}", time=0))

    # Process scale pattern
    for note, duration in data['pattern']:
        # Note on
        track.append(Message('note_on', note=note, velocity=85, time=0))
        # Note off after duration
        track.append(Message('note_off', note=note, velocity=0,
                           time=beats_to_ticks(duration, ticks_per_beat)))

    mid.save(output_path)
    print(f"✓ Exported scale: {output_path}")


def export_drum_pattern(data, output_path, ticks_per_beat=480):
    """
    Export drum pattern to MIDI file (channel 10)

    Pattern format: [
        {"drum": "kick", "note": 36, "hits": [0, 2]},
        ...
    ]
    """
    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # Add tempo
    tempo = bpm2tempo(data['tempo'])
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Add track name
    track.append(MetaMessage('track_name', name=f"{data['style']} - {data['description']}", time=0))

    # Calculate total bars and build event list
    bars = data.get('bars', 1)
    beats_per_bar = 4
    total_beats = bars * beats_per_bar

    # Build list of all events with absolute timing
    events = []
    for drum_spec in data['pattern']:
        note = drum_spec['note']
        drum_name = drum_spec['drum']

        for hit_data in drum_spec['hits']:
            # Handle both old format (just time) and new format ((time, velocity) tuple)
            if isinstance(hit_data, tuple):
                hit_time, velocity = hit_data
            else:
                # Backwards compatibility: old format with just time
                hit_time = hit_data
                velocity = 100

            # Note on event
            events.append({
                'time': hit_time,
                'type': 'note_on',
                'note': note,
                'velocity': velocity
            })
            # Note off event (short duration for drums)
            events.append({
                'time': hit_time + 0.1,
                'type': 'note_off',
                'note': note,
                'velocity': 0
            })

    # Sort events by time
    events.sort(key=lambda x: x['time'])

    # Convert to MIDI messages with delta times
    current_time = 0
    for event in events:
        delta_beats = event['time'] - current_time
        delta_ticks = beats_to_ticks(delta_beats, ticks_per_beat)

        track.append(Message(
            event['type'],
            note=event['note'],
            velocity=event['velocity'],
            time=delta_ticks,
            channel=9  # Channel 10 (0-indexed = 9) is drums
        ))

        current_time = event['time']

    # Add end_of_track marker padded to full bar length
    # This ensures MIDI clips are the correct length for grid-based DAWs
    remaining_beats = total_beats - current_time
    if remaining_beats > 0:
        remaining_ticks = beats_to_ticks(remaining_beats, ticks_per_beat)
        track.append(MetaMessage('end_of_track', time=remaining_ticks))
    else:
        track.append(MetaMessage('end_of_track', time=0))

    mid.save(output_path)
    print(f"✓ Exported drum pattern: {output_path}")


def export_rudiment(data, output_path, ticks_per_beat=480):
    """
    Export rudiment pattern to MIDI file (channel 10)

    Pattern format: [
        {"hand": "R", "note": 38, "time": 0, "duration": 0.125, "velocity": 90, "grace": false},
        ...
    ]
    """
    mid = MidiFile(ticks_per_beat=ticks_per_beat)
    track = MidiTrack()
    mid.tracks.append(track)

    # Add tempo
    tempo = bpm2tempo(data['tempo'])
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Add track name
    track_name = f"{data['name']} - {data['orchestration']} - {data['description']}"
    track.append(MetaMessage('track_name', name=track_name, time=0))

    # Build list of all events with absolute timing
    events = []
    for hit in data['pattern']:
        note = hit['note']
        time = hit['time']
        duration = hit['duration']
        velocity = hit['velocity']
        is_grace = hit.get('grace', False)

        # Note on event
        events.append({
            'time': time,
            'type': 'note_on',
            'note': note,
            'velocity': velocity,
            'is_grace': is_grace
        })
        # Note off event
        events.append({
            'time': time + duration,
            'type': 'note_off',
            'note': note,
            'velocity': 0,
            'is_grace': is_grace
        })

    # Sort events by time
    events.sort(key=lambda x: x['time'])

    # Convert to MIDI messages with delta times
    current_time = 0
    for event in events:
        delta_beats = event['time'] - current_time
        delta_ticks = beats_to_ticks(delta_beats, ticks_per_beat)

        track.append(Message(
            event['type'],
            note=event['note'],
            velocity=event['velocity'],
            time=delta_ticks,
            channel=9  # Channel 10 (0-indexed = 9) is drums
        ))

        current_time = event['time']

    mid.save(output_path)
    print(f"✓ Exported rudiment: {output_path}")


def sanitize_filename(name):
    """Remove/replace characters that are problematic in filenames"""
    replacements = {
        '/': '-',
        '\\': '-',
        ':': '',
        '*': '',
        '?': '',
        '"': '',
        '<': '',
        '>': '',
        '|': '',
        ' ': '_'
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    return name


def export_all_from_json(json_path, output_base="generated"):
    """
    Load JSON dataset and export all patterns to MIDI files
    """
    print(f"\n{'='*60}")
    print("ai_mido MIDI Exporter")
    print(f"{'='*60}\n")

    # Load dataset
    with open(json_path, 'r') as f:
        dataset = json.load(f)

    # Create output directories
    output_base = create_output_dir(output_base)
    print(f"Output directory: {output_base}\n")

    # Export chord progressions
    if 'chord_progressions' in dataset:
        print(f"Exporting {len(dataset['chord_progressions'])} chord progressions...")
        for i, progression in enumerate(dataset['chord_progressions']):
            filename = f"{i+1:02d}_{sanitize_filename(progression['key'])}_{progression['style']}.mid"
            output_path = os.path.join(output_base, "chord_progressions", filename)
            export_chord_progression(progression, output_path)

    # Export arpeggios
    if 'arpeggios' in dataset:
        print(f"\nExporting {len(dataset['arpeggios'])} arpeggios...")
        for i, arpeggio in enumerate(dataset['arpeggios']):
            filename = f"{i+1:02d}_{sanitize_filename(arpeggio['key'])}_{arpeggio['style']}.mid"
            output_path = os.path.join(output_base, "arpeggios", filename)
            export_arpeggio(arpeggio, output_path)

    # Export scales
    if 'scales' in dataset:
        print(f"\nExporting {len(dataset['scales'])} scales...")
        for i, scale in enumerate(dataset['scales']):
            filename = f"{i+1:02d}_{sanitize_filename(scale['key'])}.mid"
            output_path = os.path.join(output_base, "scales", filename)
            export_scale(scale, output_path)

    # Export drum patterns
    if 'drum_patterns' in dataset:
        print(f"\nExporting {len(dataset['drum_patterns'])} drum patterns...")
        for i, pattern in enumerate(dataset['drum_patterns']):
            filename = f"{i+1:02d}_{pattern['style']}_{pattern['tempo']}bpm.mid"
            output_path = os.path.join(output_base, "drum_patterns", filename)
            export_drum_pattern(pattern, output_path)

    # Export rudiments
    if 'rudiment_patterns' in dataset:
        print(f"\nExporting {len(dataset['rudiment_patterns'])} rudiment patterns...")
        for i, rudiment in enumerate(dataset['rudiment_patterns']):
            category = rudiment['category']
            name = sanitize_filename(rudiment['name'])
            orchestration = sanitize_filename(rudiment['orchestration'])
            usage = rudiment['usage']
            filename = f"{i+1:02d}_{category}_{name}_{orchestration}_{usage}.mid"
            output_path = os.path.join(output_base, "rudiments", filename)
            export_rudiment(rudiment, output_path)

    print(f"\n{'='*60}")
    print("Export complete!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Default: export from data/starter_dataset.json
    dataset_path = "data/starter_dataset.json"

    if os.path.exists(dataset_path):
        export_all_from_json(dataset_path)
    else:
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please ensure the dataset file exists.")
