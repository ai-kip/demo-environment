"""
AI-KIP LinkedIn Carousel PDF Converter
=======================================
Converts any carousel HTML to a LinkedIn-optimized PDF.
Uses Playwright (3x PNG screenshots) + Pillow (PDF assembly).

Usage:
    python convert.py                           # converts TEMPLATE
    python convert.py input.html                # custom input, auto output name
    python convert.py input.html output.pdf     # custom input + output

Requirements:
    pip install playwright Pillow
    playwright install chromium
"""

import sys
import tempfile
from pathlib import Path

SCALE = 3
SLIDE_W = 1080
SLIDE_H = 1350


def convert(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    from PIL import Image

    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()
    px_w, px_h = SLIDE_W * SCALE, SLIDE_H * SCALE

    print(f"[1/5] {html_file.name} -> {pdf_file.name}")
    print(f"      Scale: {SCALE}x ({px_w}x{px_h} per slide)")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--force-color-profile=srgb", "--font-render-hinting=full"],
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

        slide_count = page.locator(".slide").count()
        print(f"[2/5] {slide_count} slides, {page.evaluate('document.fonts.size')} fonts")

        tmp = Path(tempfile.mkdtemp())
        paths = []
        for i in range(slide_count):
            png = tmp / f"s{i}.png"
            page.locator(".slide").nth(i).screenshot(path=str(png), type="png")
            w, h = Image.open(png).size
            ok = "OK" if w == px_w and h == px_h else f"{w}x{h}"
            print(f"      Slide {i + 1}/{slide_count}: {ok}")
            paths.append(png)

        browser.close()

    print(f"[3/5] Building PDF ...")
    dpi = 72 * SCALE
    imgs = [Image.open(p).convert("RGB") for p in paths]
    for img in imgs:
        img.info["dpi"] = (dpi, dpi)

    imgs[0].save(str(pdf_file), "PDF", save_all=True, append_images=imgs[1:], resolution=dpi)

    for p in paths:
        p.unlink()
    tmp.rmdir()

    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    print(f"[4/5] {pdf_file.name}: {size_mb:.2f} MB {'OK' if size_mb < 10 else 'OVER 10MB!'}")
    print(f"[5/5] Done -> {pdf_file}")


if __name__ == "__main__":
    script_dir = Path(__file__).parent.resolve()

    if len(sys.argv) >= 3:
        src, dst = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        src = sys.argv[1]
        dst = Path(src).stem + ".pdf"
    else:
        src = str(script_dir / "TEMPLATE-carousel-V3.html")
        dst = str(script_dir / "TEMPLATE-carousel-V3.pdf")

    convert(src, dst)
