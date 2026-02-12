"""
AI-KIP LinkedIn Carousel PDF Converter (Vector Outlines)
=========================================================
Two-pass pipeline that produces PDFs with text as vector outlines,
matching how Canva/Adobe export PDFs (Type 3 CharProcs style).

Pipeline:
  1. Playwright: HTML -> vector PDF (Rubik+Inter TTF embedded, 1080x1350pt)
  2. Ghostscript -dNoOutputFonts: converts all font glyphs to vector paths

Result: text is stored as drawing commands, not font data.
LinkedIn doesn't need to rasterize fonts -> sharp text.

Usage:
    python convert.py input.html                # auto output name
    python convert.py input.html output.pdf     # custom output

Requirements:
    pip install playwright
    playwright install chromium
    Ghostscript (gswin64c.exe)
"""

import sys
import subprocess
import base64
import tempfile
from pathlib import Path

SLIDE_W = 1080
SLIDE_H = 1350
PDF_SCALE = 4 / 3  # CSS px -> PDF pt: 1080px=810pt, need 1080pt -> 4/3

# Ghostscript path (user-level install)
GS_BIN = Path.home() / "gs" / "bin" / "gswin64c.exe"


def _build_font_css(fonts_dir):
    """Build @font-face CSS with base64-embedded Rubik + Inter TTF fonts."""
    families = {
        "Rubik": {
            "Rubik-500.ttf": 500,
            "Rubik-600.ttf": 600,
            "Rubik-700.ttf": 700,
            "Rubik-800.ttf": 800,
        },
        "Inter": {
            "Inter-Regular.ttf": 400,
            "Inter-Medium.ttf": 500,
            "Inter-SemiBold.ttf": 600,
            "Inter-Bold.ttf": 700,
            "Inter-ExtraBold.ttf": 800,
        },
    }
    rules = []
    for family, weights in families.items():
        for filename, weight in weights.items():
            ttf_path = fonts_dir / filename
            if not ttf_path.exists():
                continue
            b64 = base64.b64encode(ttf_path.read_bytes()).decode("ascii")
            rules.append(f"""@font-face {{
                font-family: '{family}';
                font-weight: {weight};
                font-style: normal;
                font-display: block;
                src: url(data:font/truetype;base64,{b64}) format('truetype');
            }}""")
    return "\n".join(rules)


def convert(html_path, pdf_path):
    from playwright.sync_api import sync_playwright

    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()
    script_dir = Path(__file__).parent.resolve()
    fonts_dir = script_dir / "fonts"
    tmp_pdf = Path(tempfile.gettempdir()) / "carousel_pass1.pdf"

    if not GS_BIN.exists():
        print(f"ERROR: Ghostscript not found at {GS_BIN}")
        sys.exit(1)

    print(f"[1/4] {html_file.name} -> {pdf_file.name}")

    # Build font CSS
    font_css = _build_font_css(fonts_dir)

    # --- Pass 1: Playwright HTML -> vector PDF (Inter TTF) ---
    print(f"[2/4] Pass 1: HTML -> vector PDF (Playwright + Rubik/Inter TTF) ...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--force-color-profile=srgb"],
        )
        context = browser.new_context(
            viewport={"width": SLIDE_W, "height": SLIDE_H},
            color_scheme="dark",
        )
        page = context.new_page()
        page.goto(html_file.as_uri(), wait_until="networkidle")
        page.wait_for_function("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(1500)

        slide_count = page.locator(".slide").count()
        print(f"      {slide_count} slides detected")

        # Inject local TTF fonts + print styles
        page.evaluate("""(fontCSS) => {
            const style = document.createElement('style');
            style.textContent = fontCSS + `
                @page { size: 1080pt 1350pt; margin: 0; }
                @media print {
                    html, body {
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }
                    /* Prevent gradient-text bleed artifacts in PDF */
                    .headline-gradient, .label, .logo-text {
                        overflow: hidden;
                    }
                }
            `;
            document.head.appendChild(style);
        }""", font_css)

        page.wait_for_function("document.fonts.ready.then(() => true)")
        page.wait_for_timeout(500)

        page.pdf(
            path=str(tmp_pdf),
            prefer_css_page_size=True,
            scale=PDF_SCALE,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
        )
        browser.close()

    # --- Pass 2: Ghostscript converts fonts to vector outlines ---
    print(f"[3/4] Pass 2: Ghostscript -dNoOutputFonts (text -> outlines) ...")

    result = subprocess.run(
        [
            str(GS_BIN),
            "-dNoOutputFonts",
            "-dNOPAUSE",
            "-dBATCH",
            "-dQUIET",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={pdf_file}",
            str(tmp_pdf),
        ],
        capture_output=True,
        timeout=120,
    )

    tmp_pdf.unlink(missing_ok=True)

    if result.returncode != 0:
        err = result.stderr.decode("utf-8", errors="replace")
        print(f"ERROR: Ghostscript failed (exit {result.returncode}): {err}")
        sys.exit(1)

    size_mb = pdf_file.stat().st_size / (1024 * 1024)
    print(f"[4/4] {pdf_file.name}: {size_mb:.2f} MB {'OK' if size_mb < 10 else 'OVER 10MB!'}")
    print(f"      Done -> {pdf_file}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        src, dst = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        src = sys.argv[1]
        dst = Path(src).stem + ".pdf"
    else:
        print("Usage: python convert.py input.html [output.pdf]")
        sys.exit(1)

    convert(src, dst)
