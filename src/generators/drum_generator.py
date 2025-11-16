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

    # Velocity profiles for different styles
    VELOCITY_PROFILES = {
        'pop_punk': {
            'kick': {'base': 110, 'variation': 10, 'accent': 15},
            'snare': {'base': 105, 'variation': 12, 'accent': 15},
            'hihat': {'base': 75, 'variation': 15, 'accent': 20},
            'ghost_snare': {'base': 45, 'variation': 10, 'accent': 0},
        },
        'singer_songwriter': {
            'kick': {'base': 85, 'variation': 20, 'accent': 25},
            'snare': {'base': 80, 'variation': 25, 'accent': 30},
            'hihat': {'base': 60, 'variation': 20, 'accent': 25},
            'ghost_snare': {'base': 35, 'variation': 12, 'accent': 0},
        },
        'reggae_ska': {
            'kick': {'base': 95, 'variation': 18, 'accent': 20},
            'snare': {'base': 90, 'variation': 22, 'accent': 25},
            'rim': {'base': 85, 'variation': 20, 'accent': 22},
            'hihat': {'base': 70, 'variation': 18, 'accent': 28},
            'ghost_snare': {'base': 40, 'variation': 15, 'accent': 0},
        }
    }

    # Song section intensity profiles
    # Modifies density, variation, and fill_frequency based on musical context
    SECTION_PROFILES = {
        'intro': {
            'density_mult': 0.6,      # Sparse, building
            'variation_mult': 0.7,     # Somewhat repetitive
            'fill_mult': 0.8,          # Moderate fills to build tension
            'description': 'Building, sparse groove'
        },
        'verse': {
            'density_mult': 0.75,      # Supportive groove
            'variation_mult': 0.6,     # Consistent, not distracting
            'fill_mult': 0.5,          # Fewer fills, stay supportive
            'description': 'Groove-focused, supportive'
        },
        'pre_chorus': {
            'density_mult': 0.9,       # Building energy
            'variation_mult': 0.8,     # Some variation to signal change
            'fill_mult': 1.2,          # More fills to build
            'description': 'Building tension and energy'
        },
        'chorus': {
            'density_mult': 1.1,       # Full energy, driving
            'variation_mult': 0.7,     # Powerful but consistent
            'fill_mult': 0.9,          # Fills present but not overdone
            'description': 'Full energy, powerful and driving'
        },
        'bridge': {
            'density_mult': 0.85,      # Different feel
            'variation_mult': 1.3,     # High variation for contrast
            'fill_mult': 1.0,          # Transitional fills
            'description': 'Contrasting, transitional'
        },
        'breakdown': {
            'density_mult': 0.3,       # Stripped down
            'variation_mult': 0.4,     # Minimal, focused
            'fill_mult': 0.2,          # Very few fills
            'description': 'Minimal, stripped down'
        },
        'outro': {
            'density_mult': 0.7,       # Winding down or powerful ending
            'variation_mult': 0.9,     # Some variation
            'fill_mult': 1.5,          # Bigger fills for finale
            'description': 'Ending with impact or fade'
        }
    }

    def __init__(self, tempo=140, seed=None, humanize=True):
        """
        Initialize the drum generator

        Args:
            tempo: BPM
            seed: Random seed for reproducible patterns (optional)
            humanize: Apply realistic velocity humanization (default: True)
        """
        self.tempo = tempo
        self.humanize = humanize
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
                        hihat_pattern='eighth',
                        section=None):
        """
        Generate a complete drum pattern

        Args:
            style: 'pop_punk', 'singer_songwriter', 'reggae_ska', 'hybrid'
            bars: Number of bars (4/4 time)
            density: 0.0-1.0, how busy the pattern is
            variation: 0.0-1.0, how much the pattern changes
            syncopation: 0.0-1.0, amount of off-beat hits
            fill_frequency: 0.0-1.0, probability of fills
            kick_pattern: 'punk', 'four_floor', 'half_time', 'double', 'skank', 'one_drop', 'd_beat'
            hihat_pattern: 'eighth', 'sixteenth', 'ride', 'open_closed', 'skank', 'swing'
            section: Song section (optional): 'intro', 'verse', 'pre_chorus', 'chorus', 'bridge', 'breakdown', 'outro'

        Returns:
            Dictionary with pattern data ready for MIDI export
        """

        # Apply section-based intensity modifiers if section is specified
        if section and section in self.SECTION_PROFILES:
            profile = self.SECTION_PROFILES[section]
            density = min(1.0, density * profile['density_mult'])
            variation = min(1.0, variation * profile['variation_mult'])
            fill_frequency = min(1.0, fill_frequency * profile['fill_mult'])

        # Store hits with timing and velocity: {drum: [(time, velocity), ...]}
        pattern_hits = {drum: [] for drum in self.DRUMS.keys()}

        # Store style for velocity calculations
        self.current_style = style

        # Generate each bar
        for bar_num in range(bars):
            is_fill_bar = random.random() < fill_frequency
            bar_offset = bar_num * 4

            if is_fill_bar and bar_num == bars - 1:
                # Last bar fill
                self._add_fill(pattern_hits, bar_offset, style, density, bar_num, bars)
            else:
                # Regular groove
                self._add_kick(pattern_hits, bar_offset, kick_pattern, variation, syncopation, bar_num)
                self._add_snare(pattern_hits, bar_offset, style, variation, syncopation, bar_num)
                self._add_hihats(pattern_hits, bar_offset, hihat_pattern, density, variation, bar_num)

                # Add occasional cymbals
                if bar_num % 4 == 0 and bar_num > 0:
                    velocity = self._get_velocity('crash', bar_offset, is_accent=True)
                    pattern_hits['crash'].append((bar_offset, velocity))

        # Convert to the format expected by export functions with velocity
        pattern_data = []
        for drum_name, hits in pattern_hits.items():
            if hits:
                pattern_data.append({
                    'drum': drum_name,
                    'note': self.DRUMS[drum_name],
                    'hits': hits  # Now contains (time, velocity) tuples
                })

        # Build description
        description = f"Generated {style} pattern - {bars} bars"
        if section:
            section_desc = self.SECTION_PROFILES.get(section, {}).get('description', section)
            description = f"{section.replace('_', '-').title()} - {section_desc}"

        return {
            'type': 'drum_pattern',
            'tempo': self.tempo,
            'complexity': self._calculate_complexity(density, variation, syncopation),
            'style': style,
            'pattern': pattern_data,
            'bars': bars,
            'section': section,
            'humanized': self.humanize,
            'description': description
        }

    def _get_velocity(self, drum_type, time_position, is_accent=False, is_ghost=False, fill_progress=0.0):
        """
        Calculate humanized velocity for a drum hit

        Args:
            drum_type: Type of drum (kick, snare, hihat, etc.)
            time_position: Beat position in the pattern
            is_accent: Whether this is an accented hit
            is_ghost: Whether this is a ghost note (quiet)
            fill_progress: 0.0-1.0 for crescendo during fills

        Returns:
            MIDI velocity (1-127)
        """
        if not self.humanize:
            # Return static velocities if humanization is off
            if is_ghost:
                return 40
            elif is_accent:
                return 110
            else:
                return 100

        # Get velocity profile for current style
        style = self.current_style if hasattr(self, 'current_style') else 'pop_punk'

        # Map drum types to profile categories
        if 'kick' in drum_type:
            profile_key = 'kick'
        elif 'snare' in drum_type or 'rim' in drum_type:
            profile_key = 'ghost_snare' if is_ghost else 'snare'
        elif 'hihat' in drum_type or 'ride' in drum_type:
            profile_key = 'hihat'
        else:
            # Toms, cymbals, etc. - use snare profile
            profile_key = 'snare'

        # Get velocity profile, default to pop_punk if style not found
        profiles = self.VELOCITY_PROFILES.get(style, self.VELOCITY_PROFILES['pop_punk'])
        profile = profiles.get(profile_key, {'base': 90, 'variation': 15, 'accent': 20})

        # Start with base velocity
        velocity = profile['base']

        # Add accent
        if is_accent:
            velocity += profile['accent']

        # Add natural variation (Gaussian distribution for realism)
        variation_amount = profile['variation']
        velocity += random.gauss(0, variation_amount / 2.5)

        # Add subtle emphasis on downbeats (beat 1 of each bar)
        beat_position = time_position % 4
        if beat_position == 0 and not is_ghost:
            velocity += random.randint(3, 8)

        # Crescendo during fills
        if fill_progress > 0:
            velocity += fill_progress * 20

        # Slight velocity decay over long patterns (drummer fatigue)
        bar_number = int(time_position / 4)
        if bar_number > 4:
            fatigue = min((bar_number - 4) * 0.5, 8)
            velocity -= fatigue

        # Clamp to MIDI range
        velocity = max(1, min(127, int(velocity)))

        return velocity

    def _add_kick(self, pattern_hits, offset, kick_pattern, variation, syncopation, bar_num):
        """Add kick drum hits following pattern rules with humanized velocity"""

        if kick_pattern == 'punk':
            # Classic punk: 1 and 3, sometimes with syncopation
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=(bar_num % 4 == 0))
            pattern_hits['kick'].append((time, velocity))

            time = offset + 2
            velocity = self._get_velocity('kick', time)
            pattern_hits['kick'].append((time, velocity))

            # Add syncopated kicks
            if random.random() < syncopation:
                time = offset + 1.5
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))
            if random.random() < syncopation * 0.5:
                time = offset + 3.5
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))

        elif kick_pattern == 'four_floor':
            # Four on the floor
            for beat in range(4):
                time = offset + beat
                velocity = self._get_velocity('kick', time, is_accent=(beat == 0))
                pattern_hits['kick'].append((time, velocity))

        elif kick_pattern == 'half_time':
            # Half-time feel
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=True)
            pattern_hits['kick'].append((time, velocity))

            if random.random() < variation:
                time = offset + 2.5
            else:
                time = offset + 3
            velocity = self._get_velocity('kick', time)
            pattern_hits['kick'].append((time, velocity))

        elif kick_pattern == 'double':
            # Double bass punk
            for beat in [0, 0.5, 2, 2.5]:
                time = offset + beat
                velocity = self._get_velocity('kick', time, is_accent=(beat == 0))
                pattern_hits['kick'].append((time, velocity))
                if random.random() < variation * 0.3:
                    time = offset + beat + 0.25
                    velocity = self._get_velocity('kick', time)
                    pattern_hits['kick'].append((time, velocity))

        elif kick_pattern == 'skank':
            # Ska/reggae skank: emphasis on 1, groove feel
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=True)
            pattern_hits['kick'].append((time, velocity))

            # Sometimes add kick on 3 for variation
            if random.random() < variation * 0.6:
                time = offset + 2
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))

            # Subtle kick on 2.5 or 3.5 for groove
            if random.random() < syncopation * 0.7:
                time = offset + random.choice([2.5, 3.5])
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))

        elif kick_pattern == 'one_drop':
            # Reggae one-drop: NO kick on 1, heavy on 3
            time = offset + 2
            velocity = self._get_velocity('kick', time, is_accent=True)
            pattern_hits['kick'].append((time, velocity))

            # Sometimes subtle kick on 3.5 for variation
            if random.random() < variation * 0.5:
                time = offset + 3.5
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))

        elif kick_pattern == 'd_beat':
            # Hardcore d-beat: doubles the snare pattern
            # Kick on 1 and 3
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=True)
            pattern_hits['kick'].append((time, velocity))

            time = offset + 2
            velocity = self._get_velocity('kick', time, is_accent=True)
            pattern_hits['kick'].append((time, velocity))

            # Additional syncopated kicks for intensity
            if random.random() < syncopation:
                time = offset + 1.5
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))
            if random.random() < syncopation:
                time = offset + 3.5
                velocity = self._get_velocity('kick', time)
                pattern_hits['kick'].append((time, velocity))

    def _add_snare(self, pattern_hits, offset, style, variation, syncopation, bar_num):
        """Add snare hits - always on backbeat plus variations with humanized velocity"""

        # Backbeat (beats 2 and 4) - this is sacred!
        time = offset + 1
        velocity = self._get_velocity('snare', time, is_accent=True)
        pattern_hits['snare'].append((time, velocity))

        time = offset + 3
        velocity = self._get_velocity('snare', time, is_accent=True)
        pattern_hits['snare'].append((time, velocity))

        if style == 'pop_punk':
            # More aggressive, add ghost notes occasionally
            if random.random() < variation * 0.4:
                time = offset + 1.75
                velocity = self._get_velocity('snare', time, is_ghost=True)
                pattern_hits['snare'].append((time, velocity))
            if random.random() < syncopation:
                time = offset + 3.75
                velocity = self._get_velocity('snare', time)
                pattern_hits['snare'].append((time, velocity))

        elif style == 'singer_songwriter':
            # Subtle, maybe some rim clicks
            if random.random() < variation * 0.3:
                time = offset + 2
                velocity = self._get_velocity('rim', time)
                pattern_hits['rim'].append((time, velocity))

        elif style == 'reggae_ska':
            # Reggae/ska: Use rimshots (cross-stick) instead of full snare hits
            # Laid-back feel with occasional full snare for accents
            if random.random() < 0.6:
                # Beat 2 as rim click (cross-stick)
                time = offset + 1
                velocity = self._get_velocity('rim', time, is_accent=True)
                pattern_hits['rim'].append((time, velocity))
            else:
                # Sometimes full snare on 2 for accent
                time = offset + 1
                velocity = self._get_velocity('snare', time, is_accent=True)
                pattern_hits['snare'].append((time, velocity))

            if random.random() < 0.7:
                # Beat 4 as rim click
                time = offset + 3
                velocity = self._get_velocity('rim', time, is_accent=True)
                pattern_hits['rim'].append((time, velocity))
            else:
                # Sometimes full snare on 4
                time = offset + 3
                velocity = self._get_velocity('snare', time, is_accent=True)
                pattern_hits['snare'].append((time, velocity))

            # Occasional ghost notes on snare
            if random.random() < variation * 0.3:
                time = offset + 2.5
                velocity = self._get_velocity('snare', time, is_ghost=True)
                pattern_hits['snare'].append((time, velocity))

    def _add_hihats(self, pattern_hits, offset, hihat_pattern, density, variation, bar_num):
        """Add hi-hat pattern with humanized velocity"""

        if hihat_pattern == 'eighth':
            # Eighth notes
            for eighth in range(8):
                time = offset + eighth * 0.5
                if random.random() < density:
                    # Accent on downbeats (beats 1 & 3)
                    is_accent = (eighth % 4 == 0) or (eighth % 4 == 4)
                    # Occasionally open hat for variation
                    if random.random() < variation * 0.2:
                        velocity = self._get_velocity('hihat_open', time, is_accent=is_accent)
                        pattern_hits['hihat_open'].append((time, velocity))
                    else:
                        velocity = self._get_velocity('hihat_closed', time, is_accent=is_accent)
                        pattern_hits['hihat_closed'].append((time, velocity))

        elif hihat_pattern == 'sixteenth':
            # Sixteenth notes (fast punk)
            for sixteenth in range(16):
                time = offset + sixteenth * 0.25
                if random.random() < density:
                    # Accent on quarter notes
                    is_accent = (sixteenth % 4 == 0)
                    velocity = self._get_velocity('hihat_closed', time, is_accent=is_accent)
                    pattern_hits['hihat_closed'].append((time, velocity))

        elif hihat_pattern == 'ride':
            # Ride cymbal pattern
            for eighth in range(8):
                time = offset + eighth * 0.5
                if random.random() < density * 0.9:
                    is_accent = (eighth % 2 == 0)
                    velocity = self._get_velocity('ride', time, is_accent=is_accent)
                    pattern_hits['ride'].append((time, velocity))

        elif hihat_pattern == 'open_closed':
            # Alternating open/closed
            for eighth in range(8):
                time = offset + eighth * 0.5
                if eighth % 2 == 0:
                    velocity = self._get_velocity('hihat_closed', time, is_accent=True)
                    pattern_hits['hihat_closed'].append((time, velocity))
                else:
                    if random.random() < density:
                        velocity = self._get_velocity('hihat_open', time)
                        pattern_hits['hihat_open'].append((time, velocity))

        elif hihat_pattern == 'skank':
            # Ska/reggae skank: offbeats ONLY (choppy upbeat feel)
            # Hits on the "and" of each beat
            for eighth in range(8):
                if eighth % 2 == 1:  # Only odd eighths (offbeats)
                    time = offset + eighth * 0.5
                    if random.random() < density:
                        # Mostly closed, occasionally open for accent
                        if random.random() < variation * 0.25:
                            velocity = self._get_velocity('hihat_open', time, is_accent=True)
                            pattern_hits['hihat_open'].append((time, velocity))
                        else:
                            velocity = self._get_velocity('hihat_closed', time, is_accent=True)
                            pattern_hits['hihat_closed'].append((time, velocity))

        elif hihat_pattern == 'swing':
            # Swung eighth notes (triplet feel)
            # Each beat divided into triplets, playing 1st and 3rd triplet
            for beat in range(4):
                # First triplet of the beat (downbeat)
                time = offset + beat
                velocity = self._get_velocity('hihat_closed', time, is_accent=True)
                pattern_hits['hihat_closed'].append((time, velocity))

                # Third triplet of the beat (swung upbeat)
                if random.random() < density:
                    time = offset + beat + 0.667  # 2/3 of a beat for swing feel
                    # Occasionally open hat on upbeat
                    if random.random() < variation * 0.15:
                        velocity = self._get_velocity('hihat_open', time)
                        pattern_hits['hihat_open'].append((time, velocity))
                    else:
                        velocity = self._get_velocity('hihat_closed', time)
                        pattern_hits['hihat_closed'].append((time, velocity))

    def _add_fill(self, pattern_hits, offset, style, density, bar_num, total_bars):
        """Add a drum fill using rudiments-inspired patterns with crescendo"""

        fill_type = random.choice(['tom_descent', 'snare_roll', 'paradiddle', 'crash_build'])

        if fill_type == 'tom_descent':
            # Descending tom fill with crescendo
            toms = ['tom_high', 'tom_mid', 'tom_low', 'tom_floor']
            subdivisions = 8 if density > 0.6 else 4
            time_increment = 4.0 / subdivisions
            total_hits = subdivisions

            hit_count = 0
            for i, tom in enumerate(toms):
                for j in range(subdivisions // len(toms)):
                    time = offset + (i * subdivisions // len(toms) + j) * time_increment
                    fill_progress = hit_count / total_hits
                    velocity = self._get_velocity(tom, time, fill_progress=fill_progress)
                    pattern_hits[tom].append((time, velocity))
                    hit_count += 1

            # End with crash and kick
            velocity = self._get_velocity('crash', offset + 4, is_accent=True)
            pattern_hits['crash'].append((offset + 4, velocity))
            velocity = self._get_velocity('kick', offset + 4, is_accent=True)
            pattern_hits['kick'].append((offset + 4, velocity))

        elif fill_type == 'snare_roll':
            # Fast snare roll with crescendo
            subdivisions = 16 if density > 0.7 else 8
            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                fill_progress = i / subdivisions
                velocity = self._get_velocity('snare', time, fill_progress=fill_progress)
                pattern_hits['snare'].append((time, velocity))
            velocity = self._get_velocity('crash', offset + 4, is_accent=True)
            pattern_hits['crash'].append((offset + 4, velocity))

        elif fill_type == 'paradiddle':
            # Paradiddle-inspired fill (RLRR LRLL) with velocity variation
            sticking = ['snare', 'tom_high', 'snare', 'snare', 'tom_mid', 'snare', 'tom_low', 'tom_low']
            for i, drum in enumerate(sticking):
                time = offset + i * 0.5
                fill_progress = i / len(sticking)
                velocity = self._get_velocity(drum, time, fill_progress=fill_progress)
                pattern_hits[drum].append((time, velocity))
            velocity = self._get_velocity('crash', offset + 4, is_accent=True)
            pattern_hits['crash'].append((offset + 4, velocity))

        elif fill_type == 'crash_build':
            # Building crash with crescendo
            build_times = [offset + 2, offset + 2.5, offset + 3, offset + 3.5]
            for i, time in enumerate(build_times):
                fill_progress = i / len(build_times)
                velocity = self._get_velocity('snare', time, fill_progress=fill_progress)
                pattern_hits['snare'].append((time, velocity))
            velocity = self._get_velocity('crash', offset + 4, is_accent=True)
            pattern_hits['crash'].append((offset + 4, velocity))
            velocity = self._get_velocity('kick', offset + 4, is_accent=True)
            pattern_hits['kick'].append((offset + 4, velocity))

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
