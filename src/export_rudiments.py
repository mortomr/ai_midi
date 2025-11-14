#!/usr/bin/env python3
"""
ai_mido Rudiments Exporter
Exports PAS International Drum Rudiments from JSON to MIDI files using mido
"""

import os
import sys
from export_midi import export_all_from_json

if __name__ == "__main__":
    # Export rudiments from data/rudiments_dataset.json
    dataset_path = "data/rudiments_dataset.json"

    if os.path.exists(dataset_path):
        export_all_from_json(dataset_path)
    else:
        print(f"Error: Rudiments dataset not found at {dataset_path}")
        print("Please ensure the dataset file exists.")
        sys.exit(1)
