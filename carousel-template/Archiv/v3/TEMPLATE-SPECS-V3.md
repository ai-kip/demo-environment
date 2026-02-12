# AI-KIP LinkedIn Carousel Template V3

## Format

| Eigenschaft | Wert |
|---|---|
| **Breite** | 1080 px |
| **Höhe** | 1350 px |
| **Seitenverhältnis** | 4:5 (Portrait) |
| **Dateiformat** | PDF (High-Res PNG-basiert) |
| **Zielplattform** | LinkedIn Carousel |

---

## PDF-Export-Pipeline

| Schritt | Details |
|---|---|
| **Engine** | Playwright (Headless Chromium) |
| **Methode** | Screenshot jeder Slide als PNG, dann PDF-Zusammenführung |
| **Render-Scale** | 3x (3240 x 4050 px pro Slide) |
| **DPI** | 216 |
| **Farbraum** | sRGB (`--force-color-profile=srgb`) |
| **Font Hinting** | Full (`--font-render-hinting=full`) |

**Warum PNG-basiert statt Vektor-PDF?**
LinkedIn konvertiert jede PDF-Seite intern in ein JPEG-Bild. LinkedIns eigener PDF-Rasterizer produziert unscharfen Text. Durch vorgerendertes High-Res-PNG umgehen wir diesen Rasterizer und behalten volle Kontrolle über die Textqualität.

```
HTML → Playwright (3x) → PNG pro Slide → Pillow → PDF
```

### Verwendung

```bash
# Voraussetzungen (einmalig)
pip install playwright Pillow
playwright install chromium

# Konvertierung
python convert.py carousel-datei.html ausgabe.pdf
```

---

## Anti-Stitch-Technik

LinkedIn zeigt bei normalen PDFs oft horizontale Linien an Container-Grenzen ("Stitching Artifacts"). Template V3 verhindert das durch:

| Maßnahme | Details |
|---|---|
| **Einzelner Hintergrund** | `background: #111111` nur auf `<body>`, keine Slides/Container |
| **Kein Margin** | Spacing ausschließlich über `padding` (keine Lücken zwischen Boxen) |
| **Keine Borders** | Dekorative Linien via `::before`/`::after` Pseudo-Elemente |
| **Kein overflow:hidden** | Verhindert Clip-Artefakte bei Gradient-Text |
| **Ganzzahlige Pixel** | Alle CSS-Werte sind Integer (keine Sub-Pixel) |
| **Global Reset** | `border: 0; outline: 0; box-shadow: none; shape-rendering: geometricPrecision` |

---

## Layout-Struktur

```
┌──────────────────────────────────────────┐
│  80px padding (all sides)                │
│                                          │
│  [Logo] AI Knowledge &    [Slide Nr]     │  ← Header (flex row)
│          Interaction Platform            │
│                                          │
│  LABEL (gradient, uppercase)             │
│  ────── (underline, ::after)             │  ← Content (flex: 1)
│                                          │     justify-content: center
│  HEADLINE                                │
│                                          │
│  Body text                               │
│  Body text                               │
│                                          │
│  ═══════════════════════════             │  ← Flow-Line
│  Swipe →                    ai-kip.com   │  ← Footer
│                                          │
└──────────────────────────────────────────┘
```

### Bereichs-Spacing

| Bereich | Technik |
|---|---|
| **Slide → Inhalt** | `padding: 80px` auf `.slide` |
| **Header ↔ Content** | Flexbox `justify-content: center` auf `.slide-content` |
| **Label → Headline** | `padding-bottom: 48px` auf `.label` (inkl. Underline) |
| **Headline → Body** | `padding-bottom: 32px` auf `.headline` |
| **Body → Body** | `padding-bottom: 16px` auf `.body-text` |
| **Content → Footer** | Flexbox verteilt automatisch |
| **Flow-Line → Hint** | `padding-top: 16px` auf `.slide-footer` |

---

## Farbpalette

### Hintergrund

| Element | Wert |
|---|---|
| **Background** | `#111111` (nur auf `<body>`) |

### Text

| Element | Wert | Verwendung |
|---|---|---|
| **Primary** | `#FFFFFF` | Headlines, Bold |
| **Secondary** | `rgba(255,255,255, 0.72)` | Body-Text, Quotes, Bullets |
| **Muted** | `rgba(255,255,255, 0.45)` | Sublines |
| **Subtle** | `rgba(255,255,255, 0.28)` | Source-Angaben |
| **Footer** | `rgba(255,255,255, 0.22)` | Swipe-Hint |
| **Slide-Nr** | `rgba(255,255,255, 0.30)` | Slide-Nummer |

### Accent (Brand Gradient)

```css
background: linear-gradient(90deg, #00FFFF, #FF00FF);
```

| Verwendung | Technik |
|---|---|
| **Logo-Text** | `background-clip: text` |
| **Labels** | `background-clip: text` + `::after` Underline |
| **Highlight Headlines** | `background-clip: text` (Klasse `.headline-gradient`) |
| **Flow-Line** | Gradient-Background auf `.flow-line` |
| **Label-Underline** | Gradient-Background auf `.label::after` |
| **Quote-Bar** | Gradient-Background auf `.quote::before` |
| **CTA-Button** | Gradient-Background, Text `#111111` |

### Accent (Einzelfarben)

| Farbe | Hex | Verwendung |
|---|---|---|
| **Cyan** | `#00FFFF` | Bullet-Pfeile, Swipe-Pfeil, Flow-Dot Slide 1 |
| **Magenta** | `#FF00FF` | Flow-Dot Slide 8 |

---

## Typografie

### Schriftart

| Font | Typ | Quelle |
|---|---|---|
| **Inter** | Sans-Serif | Google Fonts (Open Source) |

Fallback-Stack: `'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif`

### Schriftgrößen

| Element | Größe | Gewicht | Farbe/Stil |
|---|---|---|---|
| **Logo-Text** | 18px | 700 | Gradient |
| **Slide-Nummer** | 24px | 600 | 30% White |
| **Label** | 26px | 700 | Gradient, UPPERCASE, 3px tracking |
| **Headline XL** | 72px | 800 | White oder Gradient |
| **Headline LG** | 56px | 800 | White |
| **Subline** | 38px | 400 | 45% White |
| **Body-Text** | 34px | 400 | 72% White |
| **Body Bold** | 34px | 700 | White |
| **Quote** | 32px | 400 italic | 72% White |
| **Bullets** | 32px | 400 | 72% White |
| **Source** | 22px | 400 | 28% White |
| **Swipe-Hint** | 22px | 400 | 22% White |
| **Website** | 24px | 500 | 30% White |
| **CTA-Button** | 26px | 700 | #111111 |

---

## Komponenten

### Logo-Container

```
[Logo 52px] + [14px Gap] + [AI Knowledge & Interaction Platform, 18px Gradient]
```

### Label + Underline

```
LABEL TEXT (26px, Gradient, UPPERCASE)
────────── (100px × 4px, Gradient, ::after Pseudo-Element)
[28px Abstand zur Underline + 20px zur Headline = 48px padding-bottom]
```

### Quote-Box

```css
/* Kein border! Gradient-Bar über ::before */
.quote::before {
    width: 4px;
    background: linear-gradient(180deg, #00FFFF, #FF00FF);
}
padding-left: 28px;
```

### Bullet-Points

```
→ Text (Pfeil #00FFFF via ::before, 40px padding-left)
```

### CTA-Button

```css
padding: 20px 44px;
background: linear-gradient(90deg, #00FFFF, #FF00FF);
border-radius: 14px;
color: #111111;
```

### Flow-Line

| Slide | Verhalten |
|---|---|
| **Slide 1** | 50% rechte Hälfte, Cyan-Dot (18px, Glow) links |
| **Slide 2-7** | Durchgehend 100% |
| **Slide 8** | 50% linke Hälfte, Magenta-Dot (18px, Glow) rechts |

---

## Slide-Typen

### 1. Hook-Slide (Slide 1)

- Keine Label
- Headline XL mit `.headline-gradient`
- Subline darunter
- Flow-Line startet (Cyan-Dot)

### 2. Content-Slides (Slide 2–7)

- Label + Underline (automatisch via `::after`)
- Headline LG (oder XL mit Gradient für Stat-Highlights)
- Body-Text (mehrere Absätze)
- Optional: Quote, Bullets, Source
- Flow-Line durchgehend

### 3. CTA-Slide (Slide 8)

- Keine Label
- Headline XL
- Body-Text
- CTA-Button (in `.cta-spacer` für Abstand)
- Flow-Line endet (Magenta-Dot)
- Website statt Swipe-Hint

---

## Dateien

```
carousel-template/v3/
├── TEMPLATE-carousel-V3.html    ← Master-Template (Platzhalter-Texte)
├── TEMPLATE-carousel-V3.pdf     ← Template-Export (PDF)
├── TEMPLATE-SPECS-V3.md         ← Diese Dokumentation
├── convert.py                   ← PDF-Export-Script (Playwright + Pillow)
└── carousel-*.html              ← Fertige Carousels (mit finalen Texten)
```

Logo: `carousel-template/logo.png` (im übergeordneten Ordner)

---

## Changelog

### V3 (09.02.2026)

- **Hintergrund**: Gradient-Slides → Einheitlich `#111111` (Anti-Stitch)
- **Font**: Rubik + Inter → **Inter only** (eine Familie)
- **Margin**: 50/60/80px uneinheitlich → **80px uniform** (alle Seiten)
- **Layout**: Feste Viertelhöhen → **Flexbox** (Content zentriert sich)
- **Spacing**: Margin → **Padding** durchgehend (Anti-Stitch)
- **Borders**: CSS-Border → **Pseudo-Elemente** (Anti-Stitch)
- **Overflow**: `overflow: hidden` → **entfernt** (Gradient-Text Fix)
- **PDF-Export**: Edge Headless (Vektor) → **Playwright 3x PNG** (LinkedIn-optimiert)
- **Farbraum**: Nicht spezifiziert → **sRGB** (explizit)
- **Label**: Separate Underline-Div → **`::after` Pseudo-Element**

### V2 (06.02.2026)

- Logo-Text: `AI-KIP` → `AI Knowledge & Interaction Platform`
- Logo-Text Schriftgröße: 36px → 24px

### V1 (05.02.2026)

- Initiales Template

---

## Version

- **Template-Version:** 3.0
- **Erstellt:** 05.02.2026
- **Aktualisiert:** 09.02.2026
- **Basiert auf:** AI-KIP Style Guide (Dark Mode)
