#!/usr/bin/env python3
"""Write build/icon.png — a 1024px leaf mark for electron-builder."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "icon.png"


def main() -> None:
    size = 1024
    img = Image.new("RGBA", (size, size), (20, 51, 38, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((48, 48, 976, 976), radius=180, fill=(20, 51, 38, 255))
    # Leaf body
    draw.ellipse((210, 160, 860, 880), fill=(243, 238, 228, 255))
    draw.ellipse((250, 250, 720, 900), fill=(20, 51, 38, 255))
    # Midrib
    draw.line((390, 780, 760, 240), fill=(243, 238, 228, 255), width=28)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
