"""
LinkedIn Carousel PDF Converter – Sharp Text + Anti-Stitch
===========================================================
Anti-stitching = solved in CSS (no container backgrounds, padding-only, etc.)
Text sharpness = solved here (clean Chromium rendering, no degrading flags)

Key: Do NOT use --disable-lcd-text or --disable-gpu-compositing.
Those flags killed text quality. The anti-stitch fix is 100% in the HTML/CSS.

Usage:
    python convert_sharp.py
"""

import sys
import re
from pathlib import Path


def convert():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: pip install playwright && playwright install chromium")
        sys.exit(1)

    script_dir = Path(__file__).parent.resolve()
    html_file = script_dir / "clean_carousel.html"
    pdf_file = script_dir / "linkedin_carousel_sharp.pdf"

    if not html_file.exists():
        print(f"ERROR: {html_file} not found.")
        sys.exit(1)

    print(f"[1/5] Loading {html_file.name} ...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--force-color-profile=srgb",    # sRGB color space
                "--font-render-hinting=medium",  # font hinting for crisp edges
            ],
        )

        context = browser.new_context(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=2.0,   # 2x for sharper rasterized elements (gradients, logo)
            color_scheme="dark",
        )

        page = context.new_page()
        page.emulate_media(media="screen")

        page.goto(html_file.as_uri(), wait_until="networkidle")

        # Wait for fonts
        page.wait_for_function("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(2000)

        fonts = page.evaluate("document.fonts.size")
        print(f"[2/5] Fonts loaded: {fonts} font faces")
        print("[3/5] Rendering PDF (vector text, 2x DPI for raster elements) ...")

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
    size = len(pdf_bytes)
    size_mb = size / (1024 * 1024)

    print(f"       File:      {pdf_file.name}")
    print(f"       Size:      {size:,} bytes ({size_mb:.2f} MB)")
    print(f"       < 10 MB:   {'PASS' if size_mb < 10 else 'FAIL'}")

    # Dimensions
    mediabox = re.findall(
        rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]',
        pdf_bytes,
    )
    if mediabox:
        x0, y0, w, h = (float(v) for v in mediabox[0])
        w_ok = abs(w - 810.0) < 2
        h_ok = abs(h - 1012.5) < 2
        print(f"       MediaBox:  [{x0} {y0} {w} {h}] pt = 1080x1350 px")
        print(f"       Dims:      {'PASS' if w_ok and h_ok else 'CHECK'}")
        print(f"       No margin: {'PASS' if x0 == 0 and y0 == 0 else 'FAIL'}")

    # Pages
    pages = len(re.findall(rb'/Type\s*/Page[^s]', pdf_bytes))
    print(f"       Pages:     {pages}")

    # Fonts
    font_objs = pdf_bytes.count(b"/Type /Font")
    print(f"       Fonts:     {font_objs} objects (vector)")
    print(f"       Vec text:  {'PASS' if font_objs > 0 else 'CHECK'}")

    # Images
    imgs = pdf_bytes.count(b"/Subtype /Image")
    print(f"       Images:    {imgs} (logo + gradient rasters)")

    print(f"[5/5] Done -> {pdf_file}")
    print()
    print("       Anti-stitch: CSS-based (no rendering flags needed)")
    print("       Text sharp:  Full Chromium text engine, 2x raster DPI")


if __name__ == "__main__":
    convert()
