#!/bin/bash
# Drum Generator Demo
# Shows various ways to use the generative drum engine

echo "🥁 AI_MIDO DRUM GENERATOR DEMO"
echo "================================"
echo ""

echo "1️⃣  Fast Punk Beat (high energy)"
python3 src/generate_drums.py --tempo 175 --style pop_punk --density 0.9 --variation 0.6 --bars 4

echo ""
echo "2️⃣  Mellow Singer-Songwriter (sparse, subtle)"
python3 src/generate_drums.py --tempo 72 --style singer_songwriter --density 0.3 --variation 0.2 --syncopation 0.1 --bars 8

echo ""
echo "3️⃣  Four-on-the-Floor Dance Beat"
python3 src/generate_drums.py --tempo 128 --kick four_floor --hihat sixteenth --density 0.8 --bars 8

echo ""
echo "4️⃣  Half-Time Groove"
python3 src/generate_drums.py --tempo 85 --kick half_time --hihat ride --density 0.6 --variation 0.7 --bars 4

echo ""
echo "5️⃣  Double Bass Punk Assault"
python3 src/generate_drums.py --tempo 180 --kick double --hihat sixteenth --density 1.0 --syncopation 0.5 --bars 4

echo ""
echo "6️⃣  Generate 10 Variations of the Same Style"
python3 src/generate_drums.py --tempo 140 --style pop_punk --count 10 --seed 42

echo ""
echo "✅ Demo complete! Check generated/generated_drums/ for all patterns"
