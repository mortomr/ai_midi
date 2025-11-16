#!/usr/bin/env python3
"""
Generative Drum Pattern CLI

Generate unique drum patterns using parameters instead of templates.
Every run creates something new based on music theory rules.

Usage:
    python generate_drums.py --tempo 165 --style pop_punk --density 0.8 --bars 8
    python generate_drums.py --style singer_songwriter --variation 0.3 --syncopation 0.1
    python generate_drums.py --kick four_floor --hihat sixteenth --bars 16
"""

import argparse
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generators.drum_generator import DrumPatternGenerator
from export_midi import export_drum_pattern, sanitize_filename


def main():
    parser = argparse.ArgumentParser(
        description='Generate drum patterns with controllable parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast punk beat
  python generate_drums.py --tempo 165 --style pop_punk --density 0.8

  # Mellow singer-songwriter
  python generate_drums.py --tempo 85 --style singer_songwriter --variation 0.3

  # Four-on-the-floor with sixteenth hats
  python generate_drums.py --kick four_floor --hihat sixteenth --bars 16

  # Generate 10 variations
  python generate_drums.py --count 10 --style pop_punk --density 0.7

Parameters Explained:
  density:      0.0-1.0  How busy (more notes vs. sparse)
  variation:    0.0-1.0  How much it changes (repetitive vs. dynamic)
  syncopation:  0.0-1.0  Off-beat hits (straight vs. syncopated)
  fill_frequency: 0.0-1.0  How often fills occur
        """
    )

    # Basic parameters
    parser.add_argument('--tempo', type=int, default=140,
                       help='Tempo in BPM (default: 140)')
    parser.add_argument('--style', choices=['pop_punk', 'singer_songwriter', 'reggae_ska', 'metal', 'jazz', 'rock', 'indie', 'electronic', 'hybrid'],
                       default='pop_punk',
                       help='Musical style (default: pop_punk)')
    parser.add_argument('--bars', type=int, default=4,
                       help='Number of bars (default: 4)')

    # Control parameters
    parser.add_argument('--density', type=float, default=0.7,
                       help='How busy (0.0-1.0, default: 0.7)')
    parser.add_argument('--variation', type=float, default=0.5,
                       help='How much it changes (0.0-1.0, default: 0.5)')
    parser.add_argument('--syncopation', type=float, default=0.3,
                       help='Off-beat hits (0.0-1.0, default: 0.3)')
    parser.add_argument('--fill-frequency', type=float, default=0.25,
                       help='Fill probability (0.0-1.0, default: 0.25)')

    # Pattern choices
    parser.add_argument('--kick', choices=['punk', 'four_floor', 'half_time', 'double', 'skank', 'one_drop', 'd_beat',
                                           'gallop', 'fast_double', 'sparse'],
                       default='punk',
                       help='Kick drum pattern (default: punk)')
    parser.add_argument('--hihat', choices=['eighth', 'sixteenth', 'ride', 'open_closed', 'skank', 'swing',
                                            'skate_punk', 'travis_barker', 'sparse', 'complex'],
                       default='eighth',
                       help='Hi-hat pattern (default: eighth)')

    # Song section (intensity control)
    parser.add_argument('--section', choices=['intro', 'verse', 'pre_chorus', 'chorus', 'bridge', 'breakdown', 'outro'],
                       help='Song section - auto-adjusts intensity (optional)')

    # Special modes
    parser.add_argument('--fills-only', action='store_true',
                       help='Generate only fills, no groove (perfect for 1-bar fill library)')

    # Rudiment controls
    parser.add_argument('--rudiment-type', choices=['mixed', 'rolls', 'diddles', 'flams', 'drags'],
                       default='mixed',
                       help='Rudiment flavor for fills (default: mixed)')
    parser.add_argument('--rudiment-intensity', type=float, default=0.5,
                       help='Rudiment intensity - ghost notes, accents, density (0.0-1.0, default: 0.5)')

    # Output options
    parser.add_argument('--output', '-o', type=str,
                       help='Output filename (default: auto-generated)')
    parser.add_argument('--count', type=int, default=1,
                       help='Number of variations to generate (default: 1)')
    parser.add_argument('--seed', type=int,
                       help='Random seed for reproducible patterns')

    args = parser.parse_args()

    # Validate ranges
    if not 0.0 <= args.density <= 1.0:
        parser.error('density must be between 0.0 and 1.0')
    if not 0.0 <= args.variation <= 1.0:
        parser.error('variation must be between 0.0 and 1.0')
    if not 0.0 <= args.syncopation <= 1.0:
        parser.error('syncopation must be between 0.0 and 1.0')
    if not 0.0 <= args.fill_frequency <= 1.0:
        parser.error('fill_frequency must be between 0.0 and 1.0')
    if not 0.0 <= args.rudiment_intensity <= 1.0:
        parser.error('rudiment_intensity must be between 0.0 and 1.0')

    # Create output directory
    output_dir = Path('generated/generated_drums')
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("Drum Pattern Generator")
    print(f"{'='*60}\n")
    print(f"Style: {args.style}")
    if args.section:
        print(f"Section: {args.section.replace('_', '-').title()}")
    print(f"Tempo: {args.tempo} BPM")
    print(f"Bars: {args.bars}")
    print(f"Kick: {args.kick}, Hi-hat: {args.hihat}")
    print(f"Density: {args.density:.2f}, Variation: {args.variation:.2f}, Syncopation: {args.syncopation:.2f}")
    print(f"Fill frequency: {args.fill_frequency:.2f}")
    print(f"Rudiment type: {args.rudiment_type}, Intensity: {args.rudiment_intensity:.2f}")
    if args.fills_only:
        print("Mode: Fills-only")
    print()

    # Generate patterns
    for i in range(args.count):
        # Use seed if provided, increment for each iteration
        seed = args.seed + i if args.seed is not None else None

        generator = DrumPatternGenerator(tempo=args.tempo, seed=seed)

        pattern = generator.generate_pattern(
            style=args.style,
            bars=args.bars,
            density=args.density,
            variation=args.variation,
            syncopation=args.syncopation,
            fill_frequency=args.fill_frequency,
            kick_pattern=args.kick,
            hihat_pattern=args.hihat,
            section=args.section,
            fills_only=args.fills_only,
            rudiment_type=args.rudiment_type,
            rudiment_intensity=args.rudiment_intensity
        )

        # Generate filename
        if args.output and args.count == 1:
            filename = args.output
        else:
            params_str = f"{args.style}_{args.tempo}bpm"
            if args.fills_only:
                params_str += "_FILL"
            if args.section:
                params_str += f"_{args.section}"
            params_str += f"_d{int(args.density*10)}v{int(args.variation*10)}s{int(args.syncopation*10)}"
            if args.count > 1:
                params_str += f"_var{i+1:02d}"
            filename = f"{sanitize_filename(params_str)}.mid"

        output_path = output_dir / filename

        # Export to MIDI
        export_drum_pattern(pattern, str(output_path))

    print(f"\n{'='*60}")
    print(f"Generated {args.count} pattern(s) in {output_dir}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
