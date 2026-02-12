"""
LinkedIn Carousel PDF – High-Res Image Approach
================================================
WHY: LinkedIn converts each PDF page to JPEG. Their PDF rasterizer
produces blurry text, especially gradient text on dark backgrounds.

FIX: We bypass LinkedIn's rasterizer entirely by:
1. Screenshotting each slide at 3x resolution (3240 x 4050 PNG)
2. Embedding those pixel-perfect PNGs into a PDF
3. LinkedIn now just JPEG-compresses our perfect rendering
   instead of doing its own bad rasterization

The result: 9x more pixel data -> JPEG compression has much more
to work with -> dramatically sharper text on LinkedIn.

Usage:
    python convert_hires.py
"""

import sys
import re
import tempfile
from pathlib import Path

SCALE = 3  # 3x = 3240x4050 per slide (9x pixel density)
SLIDE_W = 1080
SLIDE_H = 1350


def convert():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: pip install playwright && playwright install chromium")
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("ERROR: pip install Pillow")
        sys.exit(1)

    script_dir = Path(__file__).parent.resolve()
    html_file = script_dir / "clean_carousel.html"
    pdf_file = script_dir / "linkedin_carousel_hires.pdf"

    if not html_file.exists():
        print(f"ERROR: {html_file} not found.")
        sys.exit(1)

    print(f"[1/6] Loading {html_file.name} ...")
    print(f"       Render scale: {SCALE}x ({SLIDE_W * SCALE} x {SLIDE_H * SCALE} px per slide)")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--force-color-profile=srgb",
                "--font-render-hinting=full",
            ],
        )

        context = browser.new_context(
            viewport={"width": SLIDE_W, "height": SLIDE_H},
            device_scale_factor=SCALE,
            color_scheme="dark",
        )

        page = context.new_page()
        page.emulate_media(media="screen")
        page.goto(html_file.as_uri(), wait_until="networkidle")

        # Wait for Google Fonts
        page.wait_for_function("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(2000)

        fonts = page.evaluate("document.fonts.size")
        print(f"[2/6] Fonts loaded: {fonts} font faces")

        # Count slides
        slide_count = page.locator(".slide").count()
        print(f"[3/6] Screenshotting {slide_count} slides at {SCALE}x ...")

        slide_images = []
        tmp_dir = Path(tempfile.mkdtemp())

        for i in range(slide_count):
            slide = page.locator(".slide").nth(i)
            png_path = tmp_dir / f"slide_{i + 1}.png"

            slide.screenshot(
                path=str(png_path),
                type="png",
            )

            # Verify resolution
            img = Image.open(png_path)
            expected_w = SLIDE_W * SCALE
            expected_h = SLIDE_H * SCALE
            actual_w, actual_h = img.size

            status = "OK" if actual_w == expected_w and actual_h == expected_h else "SCALED"
            print(f"       Slide {i + 1}: {actual_w} x {actual_h} px [{status}]")

            slide_images.append(png_path)

        browser.close()

    # === Build PDF from images ===
    print(f"[4/6] Building PDF from {len(slide_images)} high-res PNGs ...")

    images = []
    for img_path in slide_images:
        img = Image.open(img_path).convert("RGB")
        # Set DPI metadata so PDF dimensions match 1080x1350 at correct DPI
        # At 3x: 3240px / 1080 CSS-px * 72 pt/inch * (1 inch / 96 CSS-px) = 72 * 3 = 216 DPI
        dpi = 72 * SCALE
        img.info["dpi"] = (dpi, dpi)
        images.append(img)

    # Save as multi-page PDF
    # Pillow embeds each image as a full page
    # Page size in points: 1080 * (72/96) = 810pt x 1350 * (72/96) = 1012.5pt
    images[0].save(
        str(pdf_file),
        "PDF",
        save_all=True,
        append_images=images[1:],
        resolution=dpi,
    )

    # Cleanup temp files
    for img_path in slide_images:
        img_path.unlink()
    tmp_dir.rmdir()

    # === Quality checks ===
    print("[5/6] Quality checks ...")

    pdf_bytes = pdf_file.read_bytes()
    size = len(pdf_bytes)
    size_mb = size / (1024 * 1024)

    print(f"       File:      {pdf_file.name}")
    print(f"       Size:      {size:,} bytes ({size_mb:.2f} MB)")
    print(f"       < 10 MB:   {'PASS' if size_mb < 10 else 'FAIL - consider SCALE=2'}")

    # Check page count
    pages = pdf_bytes.count(b"/Type /Page") - pdf_bytes.count(b"/Type /Pages")
    print(f"       Pages:     {pages}")

    # Check for image objects
    imgs = pdf_bytes.count(b"/Subtype /Image")
    print(f"       Images:    {imgs} (1 full-page image per slide)")

    # Pixel density
    print(f"       Density:   {SCALE}x ({SLIDE_W * SCALE}x{SLIDE_H * SCALE} px per page)")
    print(f"       DPI:       {72 * SCALE} (in PDF metadata)")

    print(f"[6/6] Done -> {pdf_file}")
    print()
    print("       LinkedIn will JPEG-compress our pre-rendered images")
    print(f"       instead of rasterizing vectors. {SCALE * SCALE}x more pixel data = sharper text.")


if __name__ == "__main__":
    convert()
