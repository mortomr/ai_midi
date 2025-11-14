"""
Generative Drum Pattern Engine

Creates drum patterns based on musical rules and parameters,
not static templates. Every generation is unique.
"""

import random
import json
from pathlib import Path


class DrumPatternGenerator:
    """
    Generates drum patterns using music theory rules and randomization
    """

    # General MIDI drum map
    DRUMS = {
        'kick': 36,
        'snare': 38,
        'rim': 37,
        'hihat_closed': 42,
        'hihat_open': 46,
        'hihat_pedal': 44,
        'ride': 51,
        'crash': 49,
        'tom_high': 50,
        'tom_mid': 47,
        'tom_low': 45,
        'tom_floor': 41
    }

    def __init__(self, tempo=140, seed=None):
        """
        Initialize the drum generator

        Args:
            tempo: BPM
            seed: Random seed for reproducible patterns (optional)
        """
        self.tempo = tempo
        if seed is not None:
            random.seed(seed)

    def generate_pattern(self,
                        style='pop_punk',
                        bars=4,
                        density=0.7,
                        variation=0.5,
                        syncopation=0.3,
                        fill_frequency=0.25,
                        kick_pattern='punk',
                        hihat_pattern='eighth'):
        """
        Generate a complete drum pattern

        Args:
            style: 'pop_punk', 'singer_songwriter', 'hybrid'
            bars: Number of bars (4/4 time)
            density: 0.0-1.0, how busy the pattern is
            variation: 0.0-1.0, how much the pattern changes
            syncopation: 0.0-1.0, amount of off-beat hits
            fill_frequency: 0.0-1.0, probability of fills
            kick_pattern: 'punk', 'four_floor', 'half_time', 'double'
            hihat_pattern: 'eighth', 'sixteenth', 'ride', 'open_closed'

        Returns:
            Dictionary with pattern data ready for MIDI export
        """

        pattern_hits = {drum: [] for drum in self.DRUMS.keys()}

        # Generate each bar
        for bar_num in range(bars):
            is_fill_bar = random.random() < fill_frequency
            bar_offset = bar_num * 4

            if is_fill_bar and bar_num == bars - 1:
                # Last bar fill
                self._add_fill(pattern_hits, bar_offset, style, density)
            else:
                # Regular groove
                self._add_kick(pattern_hits, bar_offset, kick_pattern, variation, syncopation)
                self._add_snare(pattern_hits, bar_offset, style, variation, syncopation)
                self._add_hihats(pattern_hits, bar_offset, hihat_pattern, density, variation)

                # Add occasional cymbals
                if bar_num % 4 == 0 and bar_num > 0:
                    pattern_hits['crash'].append(bar_offset)

        # Convert to the format expected by export functions
        pattern_data = []
        for drum_name, hits in pattern_hits.items():
            if hits:
                pattern_data.append({
                    'drum': drum_name,
                    'note': self.DRUMS[drum_name],
                    'hits': hits
                })

        return {
            'type': 'drum_pattern',
            'tempo': self.tempo,
            'complexity': self._calculate_complexity(density, variation, syncopation),
            'style': style,
            'pattern': pattern_data,
            'bars': bars,
            'description': f"Generated {style} pattern - {bars} bars"
        }

    def _add_kick(self, pattern_hits, offset, kick_pattern, variation, syncopation):
        """Add kick drum hits following pattern rules"""

        if kick_pattern == 'punk':
            # Classic punk: 1 and 3, sometimes with syncopation
            pattern_hits['kick'].append(offset + 0)  # Beat 1
            pattern_hits['kick'].append(offset + 2)  # Beat 3

            # Add syncopated kicks
            if random.random() < syncopation:
                pattern_hits['kick'].append(offset + 1.5)  # & of 2
            if random.random() < syncopation * 0.5:
                pattern_hits['kick'].append(offset + 3.5)  # & of 4

        elif kick_pattern == 'four_floor':
            # Four on the floor
            for beat in range(4):
                pattern_hits['kick'].append(offset + beat)

        elif kick_pattern == 'half_time':
            # Half-time feel
            pattern_hits['kick'].append(offset + 0)
            if random.random() < variation:
                pattern_hits['kick'].append(offset + 2.5)
            else:
                pattern_hits['kick'].append(offset + 3)

        elif kick_pattern == 'double':
            # Double bass punk
            for beat in [0, 0.5, 2, 2.5]:
                pattern_hits['kick'].append(offset + beat)
                if random.random() < variation * 0.3:
                    pattern_hits['kick'].append(offset + beat + 0.25)

    def _add_snare(self, pattern_hits, offset, style, variation, syncopation):
        """Add snare hits - always on backbeat plus variations"""

        # Backbeat (beats 2 and 4) - this is sacred!
        pattern_hits['snare'].append(offset + 1)
        pattern_hits['snare'].append(offset + 3)

        if style == 'pop_punk':
            # More aggressive, add ghost notes occasionally
            if random.random() < variation * 0.4:
                pattern_hits['snare'].append(offset + 1.75)  # Ghost note
            if random.random() < syncopation:
                pattern_hits['snare'].append(offset + 3.75)  # Pre-fill

        elif style == 'singer_songwriter':
            # Subtle, maybe some rim clicks
            if random.random() < variation * 0.3:
                pattern_hits['rim'].append(offset + 2)

    def _add_hihats(self, pattern_hits, offset, hihat_pattern, density, variation):
        """Add hi-hat pattern"""

        if hihat_pattern == 'eighth':
            # Eighth notes
            for eighth in range(8):
                time = offset + eighth * 0.5
                if random.random() < density:
                    # Occasionally open hat for variation
                    if random.random() < variation * 0.2:
                        pattern_hits['hihat_open'].append(time)
                    else:
                        pattern_hits['hihat_closed'].append(time)

        elif hihat_pattern == 'sixteenth':
            # Sixteenth notes (fast punk)
            for sixteenth in range(16):
                time = offset + sixteenth * 0.25
                if random.random() < density:
                    pattern_hits['hihat_closed'].append(time)

        elif hihat_pattern == 'ride':
            # Ride cymbal pattern
            for eighth in range(8):
                time = offset + eighth * 0.5
                if random.random() < density * 0.9:
                    pattern_hits['ride'].append(time)

        elif hihat_pattern == 'open_closed':
            # Alternating open/closed
            for eighth in range(8):
                time = offset + eighth * 0.5
                if eighth % 2 == 0:
                    pattern_hits['hihat_closed'].append(time)
                else:
                    if random.random() < density:
                        pattern_hits['hihat_open'].append(time)

    def _add_fill(self, pattern_hits, offset, style, density):
        """Add a drum fill using rudiments-inspired patterns"""

        fill_type = random.choice(['tom_descent', 'snare_roll', 'paradiddle', 'crash_build'])

        if fill_type == 'tom_descent':
            # Descending tom fill
            toms = ['tom_high', 'tom_mid', 'tom_low', 'tom_floor']
            subdivisions = 8 if density > 0.6 else 4
            time_increment = 4.0 / subdivisions

            for i, tom in enumerate(toms):
                for j in range(subdivisions // len(toms)):
                    time = offset + (i * subdivisions // len(toms) + j) * time_increment
                    pattern_hits[tom].append(time)

            # End with crash and kick
            pattern_hits['crash'].append(offset + 4)
            pattern_hits['kick'].append(offset + 4)

        elif fill_type == 'snare_roll':
            # Fast snare roll
            subdivisions = 16 if density > 0.7 else 8
            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                pattern_hits['snare'].append(time)
            pattern_hits['crash'].append(offset + 4)

        elif fill_type == 'paradiddle':
            # Paradiddle-inspired fill (RLRR LRLL)
            sticking = ['snare', 'tom_high', 'snare', 'snare', 'tom_mid', 'snare', 'tom_low', 'tom_low']
            for i, drum in enumerate(sticking):
                time = offset + i * 0.5
                pattern_hits[drum].append(time)
            pattern_hits['crash'].append(offset + 4)

        elif fill_type == 'crash_build':
            # Building crash
            pattern_hits['snare'].append(offset + 2)
            pattern_hits['snare'].append(offset + 2.5)
            pattern_hits['snare'].append(offset + 3)
            pattern_hits['snare'].append(offset + 3.5)
            pattern_hits['crash'].append(offset + 4)
            pattern_hits['kick'].append(offset + 4)

    def _calculate_complexity(self, density, variation, syncopation):
        """Calculate complexity rating 1-5"""
        score = (density + variation + syncopation) / 3
        if score < 0.3:
            return 1
        elif score < 0.5:
            return 2
        elif score < 0.7:
            return 3
        elif score < 0.85:
            return 4
        else:
            return 5


def generate_drum_pattern(tempo=140, style='pop_punk', bars=4, **kwargs):
    """
    Convenience function to generate a drum pattern

    Usage:
        pattern = generate_drum_pattern(
            tempo=165,
            style='pop_punk',
            bars=8,
            density=0.8,
            variation=0.6,
            syncopation=0.4,
            fill_frequency=0.25
        )
    """
    generator = DrumPatternGenerator(tempo=tempo)
    return generator.generate_pattern(style=style, bars=bars, **kwargs)
