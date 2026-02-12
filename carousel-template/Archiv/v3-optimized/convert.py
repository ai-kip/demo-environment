"""
LinkedIn Carousel PDF Converter
================================
Converts carousel.html → linkedin_carousel_final.pdf
using Playwright (Headless Chromium) for maximum sharpness.

Key optimizations:
- Scale 1.0 (no resampling)
- Screen media type (preserves sRGB, no CMYK conversion)
- Zero margins (no extra whitespace)
- print_background=True (preserves dark background)
- Fonts embedded as font objects (not rasterized/converted to paths)
- CSS page size respected (1080x1350px)

Usage:
    pip install playwright
    playwright install chromium
    python convert.py
"""

import os
import sys
from pathlib import Path

def convert_carousel():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        print("Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    # Paths
    script_dir = Path(__file__).parent.resolve()
    html_file = script_dir / "carousel.html"
    pdf_file = script_dir / "linkedin_carousel_final.pdf"

    if not html_file.exists():
        print(f"ERROR: {html_file} not found.")
        sys.exit(1)

    html_url = html_file.as_uri()

    print(f"[1/4] Loading {html_file.name} ...")

    with sync_playwright() as p:
        # Launch Chromium
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=1.0,       # No scaling – pixel-perfect
        )
        page = context.new_page()

        # Force screen media type (preserves sRGB colors, no CMYK shift)
        page.emulate_media(media="screen")

        # Navigate and wait for fonts to load
        page.goto(html_url, wait_until="networkidle")

        # Extra wait for Google Fonts rendering
        page.wait_for_timeout(2000)

        print("[2/4] Rendering PDF (Chromium, vector text) ...")

        # Generate PDF
        page.pdf(
            path=str(pdf_file),
            width="1080px",
            height="1350px",
            margin={
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0",
            },
            print_background=True,
            prefer_css_page_size=True,
            # tagged=True preserves text structure for accessibility
            tagged=True,
        )

        browser.close()

    # Quality checks
    print("[3/4] Quality check ...")

    file_size = pdf_file.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    print(f"       File: {pdf_file.name}")
    print(f"       Size: {file_size:,} bytes ({file_size_mb:.2f} MB)")
    print(f"       Under 10MB limit: {'YES' if file_size_mb < 10 else 'NO – too large!'}")

    # Verify PDF dimensions using basic PDF parsing
    try:
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
        # Search for MediaBox in PDF (defines page dimensions)
        import re
        mediabox_pattern = rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]'
        matches = re.findall(mediabox_pattern, pdf_bytes)
        if matches:
            x0, y0, w, h = [float(v) for v in matches[0]]
            print(f"       MediaBox: [{x0} {y0} {w} {h}] points")
            print(f"       Dimensions: {w:.0f} x {h:.0f} pt")
            # 1080x1350 px at 96dpi = 810x1012.5 pt (1pt = 1/72 inch, 1px = 1/96 inch)
            # Chromium uses 1px = 0.75pt for PDF
            expected_w = 1080 * 0.75  # 810
            expected_h = 1350 * 0.75  # 1012.5
            w_ok = abs(w - expected_w) < 2
            h_ok = abs(h - expected_h) < 2
            print(f"       Expected: {expected_w:.1f} x {expected_h:.1f} pt (= 1080x1350 px)")
            print(f"       Match: {'YES' if w_ok and h_ok else 'CHECK MANUALLY'}")
        else:
            print("       Could not parse MediaBox – check PDF manually.")
    except Exception as e:
        print(f"       PDF dimension check skipped: {e}")

    # Check for embedded fonts
    try:
        font_count = pdf_bytes.count(b"/Type /Font")
        print(f"       Embedded font objects: {font_count}")
        print(f"       Fonts as vectors: {'YES (font objects found)' if font_count > 0 else 'CHECK MANUALLY'}")
    except Exception:
        pass

    print(f"[4/4] Done! -> {pdf_file}")
    print()
    print("       Upload this file directly to LinkedIn as a document/carousel post.")

    return str(pdf_file)


if __name__ == "__main__":
    convert_carousel()
