"""
LinkedIn Carousel PDF – Maximum Sharpness
==========================================
Combines all sharpness optimizations:
1. 5x render scale (5400x6750 per slide = 25x pixel density)
2. CSS: solid cyan text, higher contrast, weight 900
3. Full font hinting, sRGB color profile
4. High-res PNG → PDF (bypasses LinkedIn's rasterizer)

Usage:
    python convert_maxsharp.py
"""

import sys
import tempfile
from pathlib import Path

SCALE = 5  # 5x = 5400x6750 per slide
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
    html_file = script_dir / "clean_carousel_maxsharp.html"
    pdf_file = script_dir / "linkedin_carousel_maxsharp.pdf"

    if not html_file.exists():
        print(f"ERROR: {html_file} not found.")
        sys.exit(1)

    px_w = SLIDE_W * SCALE
    px_h = SLIDE_H * SCALE
    print(f"[1/6] Loading {html_file.name}")
    print(f"       Scale: {SCALE}x  ({px_w} x {px_h} px per slide)")

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
        page.wait_for_function("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(2000)

        fonts = page.evaluate("document.fonts.size")
        print(f"[2/6] Fonts loaded: {fonts} faces")

        slide_count = page.locator(".slide").count()
        print(f"[3/6] Screenshotting {slide_count} slides at {SCALE}x ...")

        tmp_dir = Path(tempfile.mkdtemp())
        slide_paths = []

        for i in range(slide_count):
            png_path = tmp_dir / f"slide_{i + 1}.png"
            page.locator(".slide").nth(i).screenshot(path=str(png_path), type="png")

            img = Image.open(png_path)
            ok = img.size == (px_w, px_h)
            print(f"       Slide {i + 1}: {img.size[0]}x{img.size[1]} {'OK' if ok else 'WARN'}")
            slide_paths.append(png_path)

        browser.close()

    print(f"[4/6] Building PDF ...")

    dpi = 72 * SCALE  # 360 DPI
    images = []
    for p in slide_paths:
        img = Image.open(p).convert("RGB")
        img.info["dpi"] = (dpi, dpi)
        images.append(img)

    images[0].save(
        str(pdf_file),
        "PDF",
        save_all=True,
        append_images=images[1:],
        resolution=dpi,
    )

    # Cleanup
    for p in slide_paths:
        p.unlink()
    tmp_dir.rmdir()

    # Checks
    print("[5/6] Quality checks ...")
    size = pdf_file.stat().st_size
    size_mb = size / (1024 * 1024)

    print(f"       File:    {pdf_file.name}")
    print(f"       Size:    {size:,} bytes ({size_mb:.2f} MB)")
    print(f"       < 10 MB: {'PASS' if size_mb < 10 else 'FAIL'}")
    print(f"       Scale:   {SCALE}x ({px_w}x{px_h})")
    print(f"       DPI:     {dpi}")
    print(f"       Density: {SCALE * SCALE}x more pixels than 1x")

    print(f"[6/6] Done -> {pdf_file}")


if __name__ == "__main__":
    convert()
