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
        'kick': 36,          # C2 - Primary kick (Bass Drum 1)
        'kick_alt': 35,      # B1 - Alternate kick (Acoustic Bass Drum)
        'snare': 38,         # D2 - Primary snare (Acoustic Snare)
        'snare_alt': 40,     # E2 - Alternate snare (Electric Snare)
        'rim': 37,
        'hihat_closed': 42,
        'hihat_open': 46,
        'hihat_pedal': 44,
        'ride': 51,
        'crash': 57,  # Crash Cymbal 2 (A3) - more widely supported than 49
        'tom_high': 50,
        'tom_mid': 47,
        'tom_low': 45,
        'tom_floor': 41
    }

    # Velocity profiles for different styles
    VELOCITY_PROFILES = {
        'pop_punk': {
            'kick': {'base': 108, 'variation': 10, 'accent': 15},
            'snare': {'base': 103, 'variation': 12, 'accent': 15},
            'hihat': {'base': 92, 'variation': 15, 'accent': 20},
            'ride': {'base': 90, 'variation': 12, 'accent': 18},
            'crash': {'base': 115, 'variation': 8, 'accent': 10},
            'ghost_snare': {'base': 45, 'variation': 10, 'accent': 0},
        },
        'singer_songwriter': {
            'kick': {'base': 83, 'variation': 20, 'accent': 25},
            'snare': {'base': 78, 'variation': 25, 'accent': 30},
            'hihat': {'base': 78, 'variation': 20, 'accent': 25},
            'ride': {'base': 80, 'variation': 18, 'accent': 22},
            'crash': {'base': 95, 'variation': 15, 'accent': 20},
            'ghost_snare': {'base': 35, 'variation': 12, 'accent': 0},
        },
        'reggae_ska': {
            'kick': {'base': 93, 'variation': 18, 'accent': 20},
            'snare': {'base': 88, 'variation': 22, 'accent': 25},
            'rim': {'base': 85, 'variation': 20, 'accent': 22},
            'hihat': {'base': 88, 'variation': 18, 'accent': 28},
            'ride': {'base': 85, 'variation': 16, 'accent': 20},
            'crash': {'base': 100, 'variation': 12, 'accent': 18},
            'ghost_snare': {'base': 40, 'variation': 15, 'accent': 0},
        },
        'metal': {
            'kick': {'base': 115, 'variation': 8, 'accent': 12},
            'snare': {'base': 110, 'variation': 10, 'accent': 15},
            'hihat': {'base': 95, 'variation': 12, 'accent': 18},
            'ride': {'base': 98, 'variation': 10, 'accent': 15},
            'crash': {'base': 120, 'variation': 5, 'accent': 8},
            'ghost_snare': {'base': 50, 'variation': 8, 'accent': 0},
        },
        'jazz': {
            'kick': {'base': 70, 'variation': 25, 'accent': 30},
            'snare': {'base': 65, 'variation': 28, 'accent': 35},
            'hihat': {'base': 75, 'variation': 22, 'accent': 28},
            'ride': {'base': 85, 'variation': 18, 'accent': 25},
            'crash': {'base': 90, 'variation': 20, 'accent': 25},
            'ghost_snare': {'base': 30, 'variation': 15, 'accent': 0},
        },
        'rock': {
            'kick': {'base': 105, 'variation': 12, 'accent': 18},
            'snare': {'base': 100, 'variation': 15, 'accent': 20},
            'hihat': {'base': 88, 'variation': 16, 'accent': 22},
            'ride': {'base': 92, 'variation': 14, 'accent': 18},
            'crash': {'base': 110, 'variation': 10, 'accent': 15},
            'ghost_snare': {'base': 42, 'variation': 12, 'accent': 0},
        },
        'indie': {
            'kick': {'base': 95, 'variation': 18, 'accent': 22},
            'snare': {'base': 90, 'variation': 20, 'accent': 25},
            'hihat': {'base': 85, 'variation': 18, 'accent': 24},
            'ride': {'base': 88, 'variation': 16, 'accent': 20},
            'crash': {'base': 100, 'variation': 14, 'accent': 18},
            'ghost_snare': {'base': 38, 'variation': 14, 'accent': 0},
        },
        'electronic': {
            'kick': {'base': 112, 'variation': 5, 'accent': 8},
            'snare': {'base': 108, 'variation': 6, 'accent': 10},
            'hihat': {'base': 100, 'variation': 8, 'accent': 12},
            'ride': {'base': 102, 'variation': 7, 'accent': 10},
            'crash': {'base': 115, 'variation': 5, 'accent': 8},
            'ghost_snare': {'base': 48, 'variation': 6, 'accent': 0},
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

    def _add_drum_hit(self, pattern_hits, drum_type, time, velocity):
        """
        Add drum hit with random sample variation for kick/snare

        30% chance to use alternate sample for more natural/varied sound
        """
        if drum_type == 'kick':
            # 30% chance to use alternate kick sample
            key = 'kick_alt' if random.random() < 0.3 else 'kick'
            pattern_hits[key].append((time, velocity))
        elif drum_type == 'snare':
            # 30% chance to use alternate snare sample
            key = 'snare_alt' if random.random() < 0.3 else 'snare'
            pattern_hits[key].append((time, velocity))
        else:
            # All other drums use single sample
            pattern_hits[drum_type].append((time, velocity))

    def generate_pattern(self,
                        style='pop_punk',
                        bars=4,
                        density=0.7,
                        variation=0.5,
                        syncopation=0.3,
                        fill_frequency=0.25,
                        kick_pattern='punk',
                        hihat_pattern='eighth',
                        section=None,
                        fills_only=False,
                        rudiment_type='mixed',
                        rudiment_intensity=0.5):
        """
        Generate a complete drum pattern

        Args:
            style: 'pop_punk', 'singer_songwriter', 'reggae_ska', 'metal', 'jazz', 'rock', 'indie', 'electronic', 'hybrid'
            bars: Number of bars (4/4 time)
            density: 0.0-1.0, how busy the pattern is
            variation: 0.0-1.0, how much the pattern changes
            syncopation: 0.0-1.0, amount of off-beat hits
            fill_frequency: 0.0-1.0, probability of fills
            kick_pattern: 'punk', 'four_floor', 'half_time', 'double', 'skank', 'one_drop', 'd_beat'
            hihat_pattern: 'eighth', 'sixteenth', 'ride', 'open_closed', 'skank', 'swing'
            section: Song section (optional): 'intro', 'verse', 'pre_chorus', 'chorus', 'bridge', 'breakdown', 'outro'
            fills_only: Generate only fills, no groove (default: False)
            rudiment_type: 'mixed', 'rolls', 'diddles', 'flams', 'drags' (controls fill flavor)
            rudiment_intensity: 0.0-1.0, how prominently rudiments feature (controls ghost notes, accents)

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
            bar_offset = bar_num * 4

            if fills_only:
                # Fills-only mode: generate fill for every bar
                self._add_fill(pattern_hits, bar_offset, style, density, bar_num, bars, rudiment_type, rudiment_intensity)
            else:
                # Normal mode: groove with occasional fills
                is_fill_bar = random.random() < fill_frequency

                if is_fill_bar and bar_num == bars - 1:
                    # Last bar fill
                    self._add_fill(pattern_hits, bar_offset, style, density, bar_num, bars, rudiment_type, rudiment_intensity)
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
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            time = offset + 2
            velocity = self._get_velocity('kick', time)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            # Add syncopated kicks
            if random.random() < syncopation:
                time = offset + 1.5
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)
            if random.random() < syncopation * 0.5:
                time = offset + 3.5
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)

        elif kick_pattern == 'four_floor':
            # Four on the floor
            for beat in range(4):
                time = offset + beat
                velocity = self._get_velocity('kick', time, is_accent=(beat == 0))
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)

        elif kick_pattern == 'half_time':
            # Half-time feel
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=True)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            if random.random() < variation:
                time = offset + 2.5
            else:
                time = offset + 3
            velocity = self._get_velocity('kick', time)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

        elif kick_pattern == 'double':
            # Double bass punk
            for beat in [0, 0.5, 2, 2.5]:
                time = offset + beat
                velocity = self._get_velocity('kick', time, is_accent=(beat == 0))
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)
                if random.random() < variation * 0.3:
                    time = offset + beat + 0.25
                    velocity = self._get_velocity('kick', time)
                    self._add_drum_hit(pattern_hits, 'kick', time, velocity)

        elif kick_pattern == 'skank':
            # Ska/reggae skank: emphasis on 1, groove feel
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=True)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            # Sometimes add kick on 3 for variation
            if random.random() < variation * 0.6:
                time = offset + 2
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            # Subtle kick on 2.5 or 3.5 for groove
            if random.random() < syncopation * 0.7:
                time = offset + random.choice([2.5, 3.5])
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)

        elif kick_pattern == 'one_drop':
            # Reggae one-drop: NO kick on 1, heavy on 3
            time = offset + 2
            velocity = self._get_velocity('kick', time, is_accent=True)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            # Sometimes subtle kick on 3.5 for variation
            if random.random() < variation * 0.5:
                time = offset + 3.5
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)

        elif kick_pattern == 'd_beat':
            # Hardcore d-beat: doubles the snare pattern
            # Kick on 1 and 3
            time = offset + 0
            velocity = self._get_velocity('kick', time, is_accent=True)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            time = offset + 2
            velocity = self._get_velocity('kick', time, is_accent=True)
            self._add_drum_hit(pattern_hits, 'kick', time, velocity)

            # Additional syncopated kicks for intensity
            if random.random() < syncopation:
                time = offset + 1.5
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)
            if random.random() < syncopation:
                time = offset + 3.5
                velocity = self._get_velocity('kick', time)
                self._add_drum_hit(pattern_hits, 'kick', time, velocity)

    def _add_snare(self, pattern_hits, offset, style, variation, syncopation, bar_num):
        """Add snare hits - always on backbeat plus variations with humanized velocity"""

        # Backbeat (beats 2 and 4) - this is sacred!
        time = offset + 1
        velocity = self._get_velocity('snare', time, is_accent=True)
        self._add_drum_hit(pattern_hits, 'snare', time, velocity)

        time = offset + 3
        velocity = self._get_velocity('snare', time, is_accent=True)
        self._add_drum_hit(pattern_hits, 'snare', time, velocity)

        if style == 'pop_punk':
            # More aggressive, add ghost notes occasionally
            if random.random() < variation * 0.4:
                time = offset + 1.75
                velocity = self._get_velocity('snare', time, is_ghost=True)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)
            if random.random() < syncopation:
                time = offset + 3.75
                velocity = self._get_velocity('snare', time)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

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
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

            if random.random() < 0.7:
                # Beat 4 as rim click
                time = offset + 3
                velocity = self._get_velocity('rim', time, is_accent=True)
                pattern_hits['rim'].append((time, velocity))
            else:
                # Sometimes full snare on 4
                time = offset + 3
                velocity = self._get_velocity('snare', time, is_accent=True)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

            # Occasional ghost notes on snare
            if random.random() < variation * 0.3:
                time = offset + 2.5
                velocity = self._get_velocity('snare', time, is_ghost=True)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

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

    def _add_fill(self, pattern_hits, offset, style, density, bar_num, total_bars, rudiment_type='mixed', rudiment_intensity=0.5):
        """
        Add a drum fill using rudiments-inspired patterns with crescendo

        Args:
            rudiment_type: 'mixed', 'rolls', 'diddles', 'flams', 'drags' (controls fill flavor)
            rudiment_intensity: 0.0-1.0, how prominently rudiments feature (controls ghost notes, accents)
        """

        # Select fill type based on rudiment_type parameter
        if rudiment_type == 'rolls':
            fill_choices = ['snare_roll', 'tom_descent', 'double_stroke_roll', 'buzz_roll']
        elif rudiment_type == 'diddles':
            fill_choices = ['paradiddle', 'double_paradiddle', 'linear_fill']
        elif rudiment_type == 'flams':
            fill_choices = ['flam_tap', 'crash_build', 'flamacue']
        elif rudiment_type == 'drags':
            fill_choices = ['drag_fill', 'ruff_fill', 'snare_roll']
        else:  # mixed
            fill_choices = ['tom_descent', 'snare_roll', 'paradiddle', 'crash_build',
                          'tom_ascent', 'triplet_fill', 'linear_fill', 'double_stroke_roll',
                          'flam_tap', 'alternating_toms']

        fill_type = random.choice(fill_choices)

        # Use rudiment_intensity to control subdivision density and accent strength
        # Higher intensity = more subdivisions, stronger accents
        intensity_factor = 0.5 + (rudiment_intensity * 0.5)  # Range: 0.5 to 1.0

        if fill_type == 'tom_descent':
            # Descending tom fill with crescendo
            toms = ['tom_high', 'tom_mid', 'tom_low', 'tom_floor']
            # Intensity affects subdivision density
            base_subdivisions = 8 if density > 0.6 else 4
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(4, subdivisions)  # At least 4 hits
            time_increment = 4.0 / subdivisions
            total_hits = subdivisions

            hit_count = 0
            for i, tom in enumerate(toms):
                for j in range(subdivisions // len(toms)):
                    time = offset + (i * subdivisions // len(toms) + j) * time_increment
                    fill_progress = hit_count / total_hits
                    # Scale fill_progress by intensity for stronger crescendo
                    scaled_progress = fill_progress * intensity_factor
                    velocity = self._get_velocity(tom, time, fill_progress=scaled_progress)
                    pattern_hits[tom].append((time, velocity))
                    hit_count += 1

            # Add ghost notes between hits based on intensity
            if rudiment_intensity > 0.6:
                for i in range(subdivisions - 1):
                    if random.random() < (rudiment_intensity - 0.6) * 2:
                        time = offset + (i + 0.5) * time_increment
                        velocity = self._get_velocity('snare', time, is_ghost=True)
                        self._add_drum_hit(pattern_hits, 'snare', time, velocity)

        elif fill_type == 'snare_roll':
            # Fast snare roll with crescendo
            base_subdivisions = 16 if density > 0.7 else 8
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(8, subdivisions)  # At least 8 hits
            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                fill_progress = i / subdivisions
                # Scale fill_progress by intensity
                scaled_progress = fill_progress * intensity_factor
                velocity = self._get_velocity('snare', time, fill_progress=scaled_progress)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

            # Add grace notes/drags based on intensity
            if rudiment_intensity > 0.5:
                grace_count = int((rudiment_intensity - 0.5) * 8)
                for _ in range(grace_count):
                    grace_time = offset + random.uniform(0.5, 3.5)
                    velocity = self._get_velocity('snare', grace_time, is_ghost=True)
                    self._add_drum_hit(pattern_hits, 'snare', grace_time, velocity)

        elif fill_type == 'paradiddle':
            # Paradiddle-inspired fill (RLRR LRLL) with velocity variation
            sticking = ['snare', 'tom_high', 'snare', 'snare', 'tom_mid', 'snare', 'tom_low', 'tom_low']
            # Intensity affects timing density
            time_divisor = 0.5 * (1.0 / intensity_factor)
            for i, drum in enumerate(sticking):
                time = offset + i * time_divisor
                fill_progress = i / len(sticking)
                scaled_progress = fill_progress * intensity_factor
                # Alternate between accents based on sticking pattern
                is_accent = (i % 2 == 0) and rudiment_intensity > 0.5
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=is_accent)
                pattern_hits[drum].append((time, velocity))

        elif fill_type == 'crash_build':
            # Building crash with crescendo
            # More build hits with higher intensity
            num_hits = 4 + int(rudiment_intensity * 4)
            build_times = [offset + 2 + (i * 1.5 / num_hits) for i in range(num_hits)]
            for i, time in enumerate(build_times):
                fill_progress = i / len(build_times)
                scaled_progress = fill_progress * intensity_factor
                velocity = self._get_velocity('snare', time, fill_progress=scaled_progress)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

        elif fill_type == 'tom_ascent':
            # Ascending tom fill (opposite of descent)
            toms = ['tom_floor', 'tom_low', 'tom_mid', 'tom_high']
            base_subdivisions = 8 if density > 0.6 else 4
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(4, subdivisions)
            time_increment = 4.0 / subdivisions
            total_hits = subdivisions

            hit_count = 0
            for i, tom in enumerate(toms):
                for j in range(subdivisions // len(toms)):
                    time = offset + (i * subdivisions // len(toms) + j) * time_increment
                    fill_progress = hit_count / total_hits
                    scaled_progress = fill_progress * intensity_factor
                    velocity = self._get_velocity(tom, time, fill_progress=scaled_progress)
                    pattern_hits[tom].append((time, velocity))
                    hit_count += 1

        elif fill_type == 'triplet_fill':
            # Triplet-based fill across toms and snare
            triplets_per_beat = 3
            num_beats = 4
            total_triplets = triplets_per_beat * num_beats
            # Scale by intensity
            num_triplets = int(total_triplets * intensity_factor)
            num_triplets = max(6, num_triplets)

            drums = ['snare', 'tom_high', 'tom_mid', 'tom_low', 'tom_floor']
            for i in range(num_triplets):
                time = offset + (i / 3.0) * (4.0 / (num_triplets / 3.0))
                fill_progress = i / num_triplets
                scaled_progress = fill_progress * intensity_factor
                drum = drums[i % len(drums)]
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress)
                pattern_hits[drum].append((time, velocity))

        elif fill_type == 'linear_fill':
            # Linear fill - no simultaneous hits, alternating between drums
            base_subdivisions = 16 if density > 0.7 else 8
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(8, subdivisions)

            drums = ['snare', 'tom_high', 'hihat_closed', 'tom_mid', 'kick', 'tom_low']
            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                fill_progress = i / subdivisions
                scaled_progress = fill_progress * intensity_factor
                drum = drums[i % len(drums)]
                is_accent = (i % 4 == 0) and rudiment_intensity > 0.5
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=is_accent)

                if drum == 'kick':
                    self._add_drum_hit(pattern_hits, 'kick', time, velocity)
                else:
                    pattern_hits[drum].append((time, velocity))

        elif fill_type == 'double_stroke_roll':
            # Double stroke roll (RRLL pattern) across snare and toms
            base_subdivisions = 16 if density > 0.7 else 8
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(8, subdivisions)

            # RRLL pattern across different drums
            pattern = ['snare', 'snare', 'tom_high', 'tom_high',
                      'tom_mid', 'tom_mid', 'tom_low', 'tom_low']

            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                fill_progress = i / subdivisions
                scaled_progress = fill_progress * intensity_factor
                drum = pattern[i % len(pattern)]
                is_accent = (i % 2 == 0) and rudiment_intensity > 0.6
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=is_accent)
                pattern_hits[drum].append((time, velocity))

        elif fill_type == 'flam_tap':
            # Flam tap pattern - grace note before main note
            base_hits = 8 if density > 0.6 else 4
            num_hits = int(base_hits * intensity_factor)
            num_hits = max(4, num_hits)

            drums = ['snare', 'tom_high', 'tom_mid', 'tom_low']
            for i in range(num_hits):
                time = offset + (i / num_hits) * 4
                fill_progress = i / num_hits
                scaled_progress = fill_progress * intensity_factor
                drum = drums[i % len(drums)]

                # Grace note (flam) - only if time is positive
                if rudiment_intensity > 0.4 and time > 0.05:
                    grace_time = time - 0.05
                    grace_vel = self._get_velocity(drum, grace_time, is_ghost=True)
                    pattern_hits[drum].append((grace_time, grace_vel))

                # Main note
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=True)
                pattern_hits[drum].append((time, velocity))

        elif fill_type == 'drag_fill':
            # Drag rudiment - double grace notes before main note
            base_hits = 6 if density > 0.6 else 4
            num_hits = int(base_hits * intensity_factor)
            num_hits = max(4, num_hits)

            drums = ['snare', 'tom_high', 'tom_mid', 'tom_low']
            for i in range(num_hits):
                time = offset + (i / num_hits) * 4
                fill_progress = i / num_hits
                scaled_progress = fill_progress * intensity_factor
                drum = drums[i % len(drums)]

                # Two grace notes (drag) - only if time is positive
                if rudiment_intensity > 0.3 and time > 0.1:
                    grace1_time = time - 0.08
                    grace2_time = time - 0.04
                    grace_vel = self._get_velocity(drum, grace1_time, is_ghost=True)
                    pattern_hits[drum].append((grace1_time, grace_vel))
                    pattern_hits[drum].append((grace2_time, grace_vel))

                # Main note
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=True)
                pattern_hits[drum].append((time, velocity))

        elif fill_type == 'ruff_fill':
            # Four-stroke ruff pattern
            base_hits = 6
            num_hits = int(base_hits * intensity_factor)
            num_hits = max(4, num_hits)

            for i in range(num_hits):
                time = offset + (i / num_hits) * 4
                fill_progress = i / num_hits
                scaled_progress = fill_progress * intensity_factor

                # Three grace notes - only if time is positive
                if rudiment_intensity > 0.4 and time > 0.1:
                    for j in range(3):
                        grace_time = time - (0.03 * (3 - j))
                        grace_vel = self._get_velocity('snare', grace_time, is_ghost=True)
                        self._add_drum_hit(pattern_hits, 'snare', grace_time, grace_vel)

                # Main note
                velocity = self._get_velocity('snare', time, fill_progress=scaled_progress, is_accent=True)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

        elif fill_type == 'buzz_roll':
            # Buzz/press roll - rapid multiple bounce rolls
            base_subdivisions = 12 if density > 0.6 else 8
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(6, subdivisions)

            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                fill_progress = i / subdivisions
                scaled_progress = fill_progress * intensity_factor
                velocity = self._get_velocity('snare', time, fill_progress=scaled_progress)
                self._add_drum_hit(pattern_hits, 'snare', time, velocity)

                # Add buzz effect with ghost notes between main hits
                if rudiment_intensity > 0.5 and i < subdivisions - 1:
                    buzz_time = time + (0.5 / subdivisions)
                    buzz_vel = self._get_velocity('snare', buzz_time, is_ghost=True)
                    self._add_drum_hit(pattern_hits, 'snare', buzz_time, buzz_vel)

        elif fill_type == 'double_paradiddle':
            # Double paradiddle (RLRLRR LRLRLL)
            sticking = ['snare', 'tom_high', 'snare', 'tom_mid', 'snare', 'snare',
                       'tom_high', 'snare', 'tom_mid', 'snare', 'tom_low', 'tom_low']
            time_divisor = 0.4 * (1.0 / intensity_factor)

            for i, drum in enumerate(sticking):
                time = offset + i * time_divisor
                if time >= offset + 4:  # Don't go past the bar
                    break
                fill_progress = i / len(sticking)
                scaled_progress = fill_progress * intensity_factor
                is_accent = (i % 6 == 0) and rudiment_intensity > 0.5
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=is_accent)
                pattern_hits[drum].append((time, velocity))

        elif fill_type == 'flamacue':
            # Flamacue rudiment pattern
            base_hits = 6
            num_hits = int(base_hits * intensity_factor)
            num_hits = max(4, num_hits)

            drums = ['snare', 'tom_high', 'tom_mid', 'tom_low']
            for i in range(num_hits):
                time = offset + (i / num_hits) * 4
                fill_progress = i / num_hits
                scaled_progress = fill_progress * intensity_factor
                drum = drums[i % len(drums)]

                # Flam on first note of group - only if time is positive
                if rudiment_intensity > 0.4 and time > 0.05:
                    grace_time = time - 0.05
                    grace_vel = self._get_velocity(drum, grace_time, is_ghost=True)
                    pattern_hits[drum].append((grace_time, grace_vel))

                # Main note with accent
                velocity = self._get_velocity(drum, time, fill_progress=scaled_progress, is_accent=True)
                pattern_hits[drum].append((time, velocity))

                # Two quick taps after
                if i < num_hits - 1:
                    tap1_time = time + (0.25 / num_hits) * 4
                    tap2_time = time + (0.5 / num_hits) * 4
                    tap_vel = self._get_velocity(drum, tap1_time)
                    pattern_hits[drum].append((tap1_time, tap_vel))
                    pattern_hits[drum].append((tap2_time, tap_vel))

        elif fill_type == 'alternating_toms':
            # Alternating tom pattern with varied rhythms
            base_subdivisions = 8 if density > 0.6 else 4
            subdivisions = int(base_subdivisions * intensity_factor)
            subdivisions = max(4, subdivisions)

            # Alternate between high/low, mid/floor
            toms = ['tom_high', 'tom_low', 'tom_mid', 'tom_floor']
            for i in range(subdivisions):
                time = offset + (i / subdivisions) * 4
                fill_progress = i / subdivisions
                scaled_progress = fill_progress * intensity_factor
                tom = toms[i % len(toms)]
                is_accent = (i % 2 == 0)
                velocity = self._get_velocity(tom, time, fill_progress=scaled_progress, is_accent=is_accent)
                pattern_hits[tom].append((time, velocity))

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
