#!/usr/bin/env python3
"""
generate_chart.py

Reads skills.json and renders a sleek, GitHub-ready SVG hexagon radar chart
saved to assets/skills_chart.svg.
"""

import json
import math
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_FILE = ROOT_DIR / "skills.json"
ASSETS_DIR = ROOT_DIR / "assets"
OUTPUT_SVG = ASSETS_DIR / "skills_chart.svg"


def generate_radar_svg(data: dict) -> str:
    skills = data.get("skills", [])
    max_score = data.get("max_score", 100)
    n = len(skills)

    if n < 3:
        raise ValueError("At least 3 skills are required for a radar chart.")

    width = 560
    height = 420
    cx = width / 2
    cy = 225
    radius = 125
    levels = [0.2, 0.4, 0.6, 0.8, 1.0]

    # Calculate angles: starting from top (-pi/2)
    angles = [-math.pi / 2 + (2 * math.pi * i / n) for i in range(n)]

    # 1. Background grid concentric polygons
    grid_polygons = []
    for level in levels:
        pts = []
        r = radius * level
        for angle in angles:
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            pts.append(f"{x:.1f},{y:.1f}")
        pts_str = " ".join(pts)
        stroke_color = "#30363d" if level < 1.0 else "#484f58"
        stroke_dash = 'stroke-dasharray="3,3"' if level < 1.0 else ""
        grid_polygons.append(
            f'<polygon points="{pts_str}" fill="none" stroke="{stroke_color}" stroke-width="1" {stroke_dash} />'
        )

    # 2. Axis lines from center to outer vertices
    axis_lines = []
    for angle in angles:
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        axis_lines.append(
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#30363d" stroke-width="1" />'
        )

    # 3. Data points & polygon
    data_pts = []
    circles = []
    for i, s in enumerate(skills):
        score = min(max(s.get("score", 0), 0), max_score)
        r = radius * (score / max_score) if max_score > 0 else 0
        x = cx + r * math.cos(angles[i])
        y = cy + r * math.sin(angles[i])
        data_pts.append(f"{x:.1f},{y:.1f}")
        circles.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#38bdf8" stroke="#0d1117" stroke-width="2" />'
        )

    data_polygon_str = " ".join(data_pts)

    # 4. Labels
    labels = []
    for i, s in enumerate(skills):
        angle = angles[i]
        label_r = radius + 28
        lx = cx + label_r * math.cos(angle)
        ly = cy + label_r * math.sin(angle)

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        if cos_a > 0.2:
            anchor = "start"
        elif cos_a < -0.2:
            anchor = "end"
        else:
            anchor = "middle"

        if sin_a < -0.8:
            ly -= 5
        elif sin_a > 0.8:
            ly += 10

        name = s.get("name", f"Skill {i+1}")
        score = s.get("score", 0)

        labels.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#e6edf3" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" text-anchor="{anchor}" dominant-baseline="middle">'
            f'{name} <tspan fill="#38bdf8" font-weight="bold">({score})</tspan>'
            f'</text>'
        )

    # Calculate overall average score
    avg_score = round(sum(s.get("score", 0) for s in skills) / len(skills), 1) if skills else 0

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0.3" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Container Card -->
  <rect width="{width}" height="{height}" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />

  <!-- Header Section -->
  <text x="24" y="38" fill="#f0f6fc" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="700">🎯 Problem Solving Skill Radar</text>
  <text x="24" y="58" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="12">Overall Mastery: <tspan fill="#58a6ff" font-weight="bold">{avg_score}%</tspan> • Scale 0–{max_score}</text>

  <!-- Grid Polygons -->
  {"".join(grid_polygons)}

  <!-- Axis Lines -->
  {"".join(axis_lines)}

  <!-- Data Radar Polygon -->
  <polygon points="{data_polygon_str}" fill="url(#polyGrad)" stroke="#38bdf8" stroke-width="2.5" stroke-linejoin="round" />

  <!-- Data Point Markers -->
  {"".join(circles)}

  <!-- Labels -->
  {"".join(labels)}
</svg>
"""
    return svg_content


def main():
    if not SKILLS_FILE.exists():
        print(f"Error: {SKILLS_FILE} not found.")
        return

    with open(SKILLS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    svg_output = generate_radar_svg(data)
    OUTPUT_SVG.write_text(svg_output, encoding="utf-8")
    print(f"✨ Successfully generated radar chart at: {OUTPUT_SVG.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
