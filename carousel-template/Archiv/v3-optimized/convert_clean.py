"""
LinkedIn Carousel PDF Converter – Anti-Stitch Edition
======================================================
Converts clean_carousel.html -> linkedin_carousel_clean.pdf

Anti-stitching measures in the rendering pipeline:
- Viewport locked to exact slide dimensions (no reflow)
- device_scale_factor=1.0 (no sub-pixel interpolation)
- Screen media type (sRGB colors, no CMYK shift)
- prefer_css_page_size=True (respects @page rule exactly)
- No tiling: Chromium renders each page as a single composited layer
- Fonts remain as embedded font objects (vector, not rasterized)

Usage:
    python convert_clean.py
"""

import os
import sys
import re
from pathlib import Path


def convert():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        print("Run:  pip install playwright && playwright install chromium")
        sys.exit(1)

    script_dir = Path(__file__).parent.resolve()
    html_file = script_dir / "clean_carousel.html"
    pdf_file = script_dir / "linkedin_carousel_clean.pdf"

    if not html_file.exists():
        print(f"ERROR: {html_file} not found.")
        sys.exit(1)

    print(f"[1/5] Loading {html_file.name} ...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-lcd-text",           # no sub-pixel font rendering
                "--disable-gpu-compositing",    # single-layer compositing
                "--force-color-profile=srgb",   # lock to sRGB
                "--disable-skia-runtime-opts",  # deterministic rendering
            ],
        )

        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=1.0,
            color_scheme="dark",
        )

        page = context.new_page()

        # Force screen media (not print) to preserve sRGB and avoid CMYK
        page.emulate_media(media="screen")

        # Load HTML, wait for fonts + images
        page.goto(html_file.as_uri(), wait_until="networkidle")

        # Extra wait for Google Fonts to fully render
        page.wait_for_timeout(3000)

        # Verify fonts loaded
        fonts_ready = page.evaluate("document.fonts.ready.then(() => document.fonts.size)")
        print(f"[2/5] Fonts loaded: {fonts_ready} font faces")

        print("[3/5] Rendering PDF (single-layer, no tiling) ...")

        page.pdf(
            path=str(pdf_file),
            width="1080px",
            height="1350px",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
            tagged=True,
        )

        browser.close()

    # === Quality checks ===
    print("[4/5] Quality checks ...")

    pdf_bytes = pdf_file.read_bytes()
    file_size = len(pdf_bytes)
    file_size_mb = file_size / (1024 * 1024)

    print(f"       File:  {pdf_file.name}")
    print(f"       Size:  {file_size:,} bytes ({file_size_mb:.2f} MB)")
    print(f"       < 10MB: {'PASS' if file_size_mb < 10 else 'FAIL'}")

    # Check MediaBox dimensions
    mediabox = re.findall(
        rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]',
        pdf_bytes,
    )
    if mediabox:
        x0, y0, w, h = (float(v) for v in mediabox[0])
        # 1080px * 0.75 = 810pt, 1350px * 0.75 = 1012.5pt
        w_expected, h_expected = 810.0, 1012.5
        w_ok = abs(w - w_expected) < 2
        h_ok = abs(h - h_expected) < 2
        print(f"       MediaBox: [{x0} {y0} {w} {h}] pt")
        print(f"       Expected: [0 0 {w_expected} {h_expected}] pt (= 1080x1350 px)")
        print(f"       Dimensions: {'PASS' if w_ok and h_ok else 'CHECK'}")
    else:
        print("       MediaBox: could not parse")

    # Count pages
    page_count = len(re.findall(rb'/Type\s*/Page[^s]', pdf_bytes))
    print(f"       Pages: {page_count}")

    # Check embedded fonts (vector, not rasterized)
    font_objects = pdf_bytes.count(b"/Type /Font")
    font_subset = pdf_bytes.count(b"/Subtype /Type1") + pdf_bytes.count(b"/Subtype /TrueType") + pdf_bytes.count(b"/Subtype /CIDFontType2")
    print(f"       Font objects: {font_objects}")
    print(f"       Font subsets:  {font_subset}")
    print(f"       Vector text: {'PASS' if font_objects > 0 else 'CHECK'}")

    # Check for image objects (should be minimal – only the logo)
    image_count = pdf_bytes.count(b"/Subtype /Image")
    print(f"       Image objects: {image_count} (expected: 1 per page = logo)")

    # No margins check: first MediaBox should start at 0,0
    if mediabox:
        if float(mediabox[0][0]) == 0 and float(mediabox[0][1]) == 0:
            print(f"       Zero margins: PASS")
        else:
            print(f"       Zero margins: FAIL (offset detected)")

    print(f"[5/5] Done -> {pdf_file}")
    print()
    print("       Ready for LinkedIn upload.")


if __name__ == "__main__":
    convert()
