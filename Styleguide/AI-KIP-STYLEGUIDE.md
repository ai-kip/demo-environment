# AI Knowledge & Interaction Platform — Brand Style Guide

> **Version:** 1.0 | **Date:** 2026-02-09
> **Applies to:** LinkedIn Carousels, HTML Emails, Brochures, Slide Decks, Social Graphics, Landing Pages

---

## 1. Design Philosophy

AI-KIP's visual language communicates **intelligence, precision, and trust**. The design draws from two complementary modes:

| Context | Mode | When to Use |
|---------|------|-------------|
| **Marketing / External** | Dark Mode | Carousels, social media, brochures, pitch decks, ads |
| **Product / Internal** | Light Mode | Web app, dashboards, documentation, internal emails |

Both modes share the same **typography, spacing grid, and brand gradient** — only the background and text color palette shift.

---

## 2. Logo

| Element | Specification |
|---------|---------------|
| **File** | `logo.png` (transparent PNG) |
| **Icon Size** | 72px height (marketing), 32–40px (product UI) |
| **Logo Text** | "AI Knowledge & Interaction Platform" |
| **Logo Font** | Rubik 700, gradient fill |
| **Gap** | 18px between icon and text |
| **Minimum Clear Space** | 1× icon height on all sides |

### Logo-Text Rendering (CSS)

```css
.logo-text {
    font-family: 'Rubik', sans-serif;
    font-weight: 700;
    font-size: 24px;  /* scale proportionally per format */
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

### Print / Email Fallback

When CSS gradient-text is not supported, use **#00CCCC** (Cyan) as a flat color for the logo text.

---

## 3. Color Palette

### 3.1 Brand Gradient (Primary Identity)

```css
background: linear-gradient(90deg, #00FFFF, #FF00FF);
```

| Token | Hex | Role |
|-------|-----|------|
| **Accent Cyan** | `#00FFFF` | Gradient start, data highlights, interactive elements |
| **Accent Magenta** | `#FF00FF` | Gradient end, energy, urgency |

**Usage:** Logo text, labels, CTA buttons (background), flow-lines, decorative accents, key stat highlights.

**Never** use the gradient for body text or large background fills.

### 3.2 Dark Mode (Marketing Materials)

#### Backgrounds

| Token | Hex | Usage |
|-------|-----|-------|
| **Base Dark** | `#0B0F1A` | Primary background, slide/page start |
| **Deep Navy** | `#141F40` | Mid-range backgrounds |
| **Rich Indigo** | `#242C62` | Late-section backgrounds |
| **Deep Purple** | `#302F75` | Final section / CTA background |

For multi-page materials (carousels, brochures), the background **gradually shifts** from Base Dark → Deep Purple to create a visual journey. Single-page formats should use `#0B0F1A` or `#0F1A35`.

#### Background Glow (Ambient Light)

Subtle radial gradients add depth. Each page/section gets a soft glow:

```css
/* Early sections: Cyan glow */
background: radial-gradient(ellipse at 10% 90%, rgba(0, 255, 255, 0.12) 0%, transparent 50%);

/* Mid sections: Blue/Purple glow */
background: radial-gradient(ellipse at 70% 50%, rgba(60, 97, 238, 0.12) 0%, transparent 50%);

/* Late sections: Magenta glow */
background: radial-gradient(ellipse at 95% 15%, rgba(255, 0, 255, 0.15) 0%, transparent 50%);
```

#### Text Colors (Dark Mode)

| Token | Hex | Usage |
|-------|-----|-------|
| **Text Primary** | `#F2F4F8` | Headlines, primary content |
| **Text Secondary** | `#C8CDD5` | Body text, descriptions |
| **Text Muted** | `#A0A7B5` | Sublines, secondary info |
| **Text Subtle** | `#7A8290` | Source citations, metadata |
| **Text Footer** | `#6A7080` | Navigation hints, footers |
| **Text Website** | `#8A90A0` | URLs, tertiary info |
| **Bold/Emphasis** | `#FFFFFF` | `<strong>` text within body |

### 3.3 Light Mode (Product / Email)

| Token | CSS Variable | Hex | Usage |
|-------|-------------|-----|-------|
| **Background** | `--color-white` | `#FFFFFF` | Page background |
| **Surface** | `--color-snow` | `#F8FAFC` | Cards, sections |
| **Surface Alt** | `--color-mist` | `#F1F5F9` | Alternating rows, hover |
| **Border** | `--color-silver` | `#E2E8F0` | Dividers, borders |
| **Text Primary** | `--color-text-primary` | `#111827` | Headlines, body |
| **Text Secondary** | `--color-gray` | `#64748B` | Descriptions, meta |
| **Text Tertiary** | `--color-slate` | `#94A3B8` | Placeholders, hints |
| **Primary Blue** | `--color-deep-ocean` | `#0A1628` | Deep brand dark (headers) |
| **Action Blue** | `--color-trust-blue` | `#2563EB` | Links, primary buttons |

### 3.4 Semantic Colors (Both Modes)

| Token | Hex | Usage |
|-------|-----|-------|
| **Success** | `#10B981` | Positive signals, confirmations |
| **Warning** | `#F59E0B` | Attention, caution |
| **Error** | `#EF4444` | Errors, critical alerts |
| **Info** | `#6366F1` | Informational highlights |

---

## 4. Typography

### 4.1 Font Families

| Font | Role | Source |
|------|------|--------|
| **Rubik** | Headlines, labels, logo text, buttons, display numbers | Google Fonts / local TTF |
| **Inter** | Body text, sublines, captions, UI text | Google Fonts / local TTF |

**Fallback stack:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

### 4.2 Type Scale — Marketing (Dark Mode)

Designed for 1080px-wide formats. Scale proportionally for other sizes.

| Element | Font | Size | Weight | Line-Height | Color | Letter-Spacing |
|---------|------|------|--------|-------------|-------|----------------|
| **Headline XL** | Rubik | 76px | 700 | 1.05 | `#F2F4F8` or Gradient | -0.02em |
| **Headline LG** | Rubik | 62px | 700 | 1.05 | `#F2F4F8` | -0.02em |
| **Headline MD** | Rubik | 48px | 700 | 1.1 | `#F2F4F8` | -0.02em |
| **Label** | Rubik | 36px | 700 | 1.2 | Gradient | 0 |
| **Subline** | Inter | 44px | 400 | 1.4 | `#A0A7B5` | 0 |
| **Body** | Inter | 38px | 400 | 1.5 | `#C8CDD5` | 0 |
| **Body Bold** | Inter | 38px | 600 | 1.5 | `#FFFFFF` | 0 |
| **Quote** | Inter | 36px | 400 italic | 1.45 | `#C8CDD5` | 0 |
| **Bullet** | Inter | 36px | 400 | 1.45 | `#C8CDD5` | 0 |
| **Source** | Inter | 26px | 400 | 1.4 | `#7A8290` | 0 |
| **Slide Number** | Rubik | 32px | 600 | 1.0 | `#00FFFF` | 0 |
| **Swipe Hint** | Inter | 28px | 400 | 1.0 | `#6A7080` | 0 |
| **Website** | Inter | 32px | 500 | 1.0 | `#8A90A0` | 0 |
| **CTA Button** | Rubik | 28px | 700 | 1.0 | `#0B0F1A` | 0 |

### 4.3 Type Scale — Product / Email (Light Mode)

| Element | Font | Size | Weight | Line-Height |
|---------|------|------|--------|-------------|
| **Display** | Rubik | 48px | 700 | 1.1 |
| **H1** | Rubik | 32px | 700 | 1.2 |
| **H2** | Rubik | 24px | 700 | 1.3 |
| **H3** | Rubik | 20px | 600 | 1.4 |
| **H4** | Inter | 16px | 600 | 1.5 |
| **Body Large** | Inter | 16px | 400 | 1.6 |
| **Body** | Inter | 14px | 400 | 1.6 |
| **Body Small** | Inter | 13px | 400 | 1.6 |
| **Caption** | Inter | 12px | 400 | 1.4 |
| **Overline** | Inter | 11px | 600 | 1.3 |

### 4.4 Scaling for Other Formats

| Format | Base Width | Scale Factor | Headline XL → |
|--------|-----------|-------------|---------------|
| LinkedIn Carousel | 1080px | 1.0× | 76px |
| A4 Brochure (portrait) | ~794px | 0.73× | 56px |
| HTML Email (600px) | 600px | 0.55× | 42px |
| Instagram Story | 1080px | 1.0× | 76px |
| Slide Deck (1920px) | 1920px | 1.78× | 76px (cap) |

**Rule:** Never exceed 76px for headlines regardless of format width. Scale down proportionally; don't scale up.

---

## 5. Spacing System

### 5.1 Base Grid

**8px base grid.** All spacing values are multiples of 4 or 8.

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Inline gaps, icon padding |
| `space-2` | 8px | Tight element spacing |
| `space-3` | 12px | Label-to-underline gap |
| `space-4` | 16px | Source citation margin-top |
| `space-5` | 24px | Paragraph spacing, bullet margin, quote margin |
| `space-6` | 32px | Section gaps (label-underline to headline) |
| `space-7` | 48px | Major section breaks, CTA button padding-x |
| `space-8` | 64px | Page margins (large format) |
| `space-9` | 96px | Hero spacing |

### 5.2 Page Margins by Format

| Format | Top | Sides | Bottom |
|--------|-----|-------|--------|
| Carousel (1080×1350) | 50px | 60–80px | 50px |
| A4 Brochure | 40px | 50px | 40px |
| HTML Email (600px) | 32px | 24–32px | 32px |
| Slide Deck | 60px | 80px | 60px |

---

## 6. Components

### 6.1 Label with Underline

A category tag above a headline. Always uses the brand gradient.

```
[Label Text — 36px Rubik 700, Gradient]
[────── 130px × 6px bar, Gradient, border-radius: 3px]
[32px gap]
[Headline]
```

```css
.label {
    font-family: 'Rubik', sans-serif;
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
}

.label-underline {
    width: 130px;
    height: 6px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    border-radius: 3px;
    margin-bottom: 32px;
}
```

**Print/email fallback:** Use a solid `#00CCCC` bar if gradients are unsupported.

### 6.2 Quote Box

Left-bordered quote for testimonials, examples, or highlighted text.

```css
.quote {
    font-family: 'Inter', sans-serif;
    font-size: 36px;  /* scale per format */
    color: #C8CDD5;
    font-style: italic;
    padding-left: 36px;
    border-left: 6px solid;
    border-image: linear-gradient(180deg, #00FFFF, #FF00FF) 1;
    margin: 24px 0;
    line-height: 1.45;
}
```

**Print/email fallback:** Use `border-left: 6px solid #00CCCC;` (flat color).

### 6.3 Bullet Points

Arrow-style bullets with cyan accent.

```
→ Item text
→ Item text
→ Item text
```

```css
.bullets li::before {
    content: '→';
    color: #00FFFF;
    font-weight: bold;
    font-size: 38px;  /* scale per format */
}
```

**Print/email alternative:** Use `▸` or `›` if arrow rendering is inconsistent. Always `#00FFFF` colored.

### 6.4 CTA Button

```css
.cta-button {
    padding: 24px 48px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    border-radius: 16px;
    font-family: 'Rubik', sans-serif;
    font-size: 28px;  /* scale per format */
    color: #0B0F1A;
    font-weight: 700;
    text-decoration: none;
    display: inline-block;
}
```

**Email fallback (VML/MSO):**
```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" style="height:60px;width:240px;" arcsize="25%" fillcolor="#00CCCC" stroke="f">
  <v:textbox><center style="color:#0B0F1A;font-family:Arial;font-size:16px;font-weight:bold;">Book a Demo</center></v:textbox>
</v:roundrect>
<![endif]-->
```

### 6.5 Flow Line (Carousel-Specific)

A gradient progress bar that connects slides visually.

```css
.flow-line {
    height: 6px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
}
```

| Slide | Behavior |
|-------|----------|
| First | Starts at 50%, cyan dot (26px) with glow on left |
| Middle | Full width |
| Last | Ends at 50%, magenta dot (26px) with glow on right |

For non-carousel formats, use a single 6px gradient line as a **section divider**.

### 6.6 Source Citation

```css
.source {
    font-family: 'Inter', sans-serif;
    font-size: 26px;  /* scale per format */
    color: #7A8290;
    margin-top: 16px;
}
```

Format: `— Source Name "Publication" (Year)`

### 6.7 Stat/Number Highlight

Large numbers or percentages should use **Rubik 700** at headline sizes with the gradient fill for maximum impact.

```
[76px Rubik 700, Gradient]  3× Higher ROI
[38px Inter 400, #C8CDD5]   Supporting explanation text
```

---

## 7. Layout Patterns

### 7.1 Carousel Slide (1080 × 1350px)

```
┌──────────────────────────────────────┐  ─┐
│  [Logo] AI Knowledge &     [N/8]    │   │ HEADER (337px)
│         Interaction Platform         │   │ padding: 50px 60px
├──────────────────────────────────────┤  ─┤
│  Label                               │   │
│  ───────                             │   │ CONTENT (675px)
│  HEADLINE                            │   │ padding: 0 80px
│  Body text                           │   │
├──────────────────────────────────────┤  ─┤
│  ════════════════════════════════    │   │ FOOTER (338px)
│  Swipe →                             │   │ flow-line at 120px
└──────────────────────────────────────┘  ─┘
```

### 7.2 Email Layout (600px wide)

```
┌──────────────────────────────────────┐
│  [Logo] AI Knowledge &               │ Header: bg #0B0F1A
│         Interaction Platform         │ padding: 24px
├──────────────────────────────────────┤
│                                      │
│  Label                               │ Content: bg #0F1A35
│  ───────                             │ padding: 32px 24px
│  Headline                            │
│  Body text                           │
│                                      │
│       [ CTA Button ]                 │
│                                      │
├──────────────────────────────────────┤
│  ai-kip.com | Unsubscribe           │ Footer: bg #0B0F1A
│                                      │ padding: 16px 24px
└──────────────────────────────────────┘
```

### 7.3 Brochure / One-Pager (A4)

```
┌──────────────────────────────────────┐
│  [Logo]                    [Tagline] │ Header band
│  ════════════════════════════════    │ gradient divider (4px)
├──────────────────────────────────────┤
│                                      │
│  HERO HEADLINE (gradient)            │ Hero section
│  Subline                             │ bg: #0B0F1A
│                                      │
├──────────────────────────────────────┤
│  ┌──────┐ ┌──────┐ ┌──────┐        │ Feature columns
│  │ Icon │ │ Icon │ │ Icon │        │ bg: #0F1A35
│  │ Head │ │ Head │ │ Head │        │
│  │ Text │ │ Text │ │ Text │        │
│  └──────┘ └──────┘ └──────┘        │
├──────────────────────────────────────┤
│  Quote / Testimonial                 │ Social proof
│  ─ Source                            │ bg: #141F40
├──────────────────────────────────────┤
│       [ CTA Button ]                 │ CTA section
│  ai-kip.com                          │ bg: #192448
└──────────────────────────────────────┘
```

---

## 8. Format-Specific Guidelines

### 8.1 LinkedIn Carousels

- **Size:** 1080 × 1350px (4:5 portrait)
- **Export:** PDF, text as vector outlines (Ghostscript `-dNoOutputFonts`)
- **Max file size:** 10 MB (LinkedIn limit)
- **Slide count:** 8 slides (optimal for engagement)
- **Slide structure:** Hook → Problem → Content → Solution → CTA
- **Always include:** Logo + slide number in header, flow-line in footer
- **Swipe hint:** "Swipe →" on slides 1–7, website URL on slide 8

### 8.2 HTML Emails

- **Width:** 600px (max), fluid to 320px minimum
- **Background:** Use solid `#0B0F1A` (no CSS gradients in email body — some clients strip them)
- **Fonts:** Rubik/Inter via web font `<link>` in `<head>`, fallback to Arial/Helvetica
- **Images:** All images must have `alt` text; use retina-ready (2×) images
- **CTA buttons:** Use VML fallback for Outlook (see 6.4 above)
- **Gradient accent:** Use a pre-rendered gradient PNG strip (6px tall) for dividers
- **Dark mode support:** Include `@media (prefers-color-scheme: dark)` overrides
- **Max email width:** 600px, center-aligned on larger screens

### 8.3 Brochures / Print

- **Color space:** Convert hex values to CMYK for professional printing
- **Approximate CMYK conversions:**
  - `#0B0F1A` → C:90 M:80 K:85 (Rich Black)
  - `#00FFFF` → C:100 M:0 Y:0 K:0 (Process Cyan)
  - `#FF00FF` → C:0 M:100 Y:0 K:0 (Process Magenta)
  - `#F2F4F8` → C:2 M:1 Y:0 K:2
- **Bleed:** 3mm on all sides
- **Resolution:** 300 DPI minimum for all raster elements
- **Logo:** Use vector (SVG/EPS) version where available
- **Gradient bar:** Reproducible in CMYK as Cyan → Magenta

### 8.4 Slide Decks / Presentations

- **Size:** 16:9 (1920 × 1080) or 4:3 (1440 × 1080)
- **Background:** Single dark value per slide (no per-slide gradient progression needed)
- **Title slides:** Use Headline XL (capped at 76px) with gradient
- **Content slides:** Use Headline LG + body text
- **Use the gradient bar** as a consistent bottom divider on every slide

### 8.5 Social Media Graphics

| Platform | Size | Notes |
|----------|------|-------|
| LinkedIn Post | 1200 × 627px | Landscape, single message |
| LinkedIn Carousel | 1080 × 1350px | Portrait, multi-slide |
| Instagram Post | 1080 × 1080px | Square, adapt layout |
| Instagram Story | 1080 × 1920px | Vertical, more space |
| Twitter/X | 1200 × 675px | Landscape |

---

## 9. Do's and Don'ts

### Do

- Use the Cyan → Magenta gradient for **accents and highlights only**
- Keep headlines short and punchy (2–4 lines max)
- Bold (`<strong>`) key phrases strategically — 1–2 per paragraph
- Maintain generous whitespace — let content breathe
- Use consistent slide/section structure across materials
- Include source citations for all statistics
- Test dark mode rendering in email clients

### Don't

- Don't use the gradient as a full background fill
- Don't mix Light Mode and Dark Mode within one document
- Don't use more than 2 font families (Rubik + Inter)
- Don't use font weights below 400 or above 800
- Don't place body text directly on the gradient
- Don't use colored body text (stick to the defined text color hierarchy)
- Don't center-align body text — always left-aligned
- Don't use all-caps for body text (reserved for overlines/labels if needed)

---

## 10. File & Asset Reference

```
carousel-template/
├── Template final/
│   ├── TEMPLATE-carousel-final.html   ← Master carousel template
│   ├── TEMPLATE-carousel-final.pdf    ← Reference export
│   ├── TEMPLATE-SPECS-final.md        ← Carousel-specific spec
│   ├── convert.py                     ← HTML → PDF pipeline
│   ├── generate_carousels.py          ← Batch carousel generator
│   ├── fonts/                         ← Rubik + Inter TTF files
│   └── logo.png                       ← AI-KIP logo
├── Output final/                      ← Generated carousel PDFs
├── AI-KIP-STYLEGUIDE.md              ← This document
└── AI-KIP LINKEDIN CAROUSELS final.txt ← Carousel content
```

### Font Files Required

| Font | Files | Weights |
|------|-------|---------|
| **Rubik** | `Rubik-500.ttf` through `Rubik-800.ttf` | 500, 600, 700, 800 |
| **Inter** | `Inter-Regular.ttf` through `Inter-ExtraBold.ttf` | 400, 500, 600, 700, 800 |

### Google Fonts Import

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Rubik:wght@500;600;700;800&display=swap" rel="stylesheet">
```

---

## 11. Quick-Reference: CSS Custom Properties

For web-based formats, these CSS custom properties provide the complete token set:

```css
:root {
    /* Brand Gradient */
    --brand-gradient: linear-gradient(90deg, #00FFFF, #FF00FF);
    --accent-cyan: #00FFFF;
    --accent-magenta: #FF00FF;
    --accent-cyan-flat: #00CCCC;  /* email/print fallback */

    /* Dark Mode Backgrounds */
    --bg-dark-base: #0B0F1A;
    --bg-dark-deep: #0F1A35;
    --bg-dark-mid: #192448;
    --bg-dark-rich: #242C62;
    --bg-dark-end: #302F75;

    /* Dark Mode Text */
    --text-dark-primary: #F2F4F8;
    --text-dark-secondary: #C8CDD5;
    --text-dark-muted: #A0A7B5;
    --text-dark-subtle: #7A8290;
    --text-dark-footer: #6A7080;
    --text-dark-bold: #FFFFFF;

    /* Light Mode Backgrounds */
    --bg-light-base: #FFFFFF;
    --bg-light-surface: #F8FAFC;
    --bg-light-alt: #F1F5F9;
    --bg-light-border: #E2E8F0;

    /* Light Mode Text */
    --text-light-primary: #111827;
    --text-light-secondary: #64748B;
    --text-light-tertiary: #94A3B8;
    --text-light-action: #2563EB;

    /* Typography */
    --font-display: 'Rubik', sans-serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

    /* Spacing (8px grid) */
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 24px;
    --space-6: 32px;
    --space-7: 48px;
    --space-8: 64px;

    /* Radii */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-full: 9999px;
}
```

---

*This style guide is the single source of truth for all AI-KIP visual design decisions. When in doubt, refer to the carousel template as the canonical dark-mode reference and the platform design tokens (`design-tokens.css`) as the canonical light-mode reference.*
