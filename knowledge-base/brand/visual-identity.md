# Visual Identity -- How We Look

> **Last updated:** 2026-02-09
> **Full design system:** See `Styleguide/AI-KIP-STYLEGUIDE.md`
> **Web UX/UI specs:** See Style Guide Web (Light & Dark Mode) PDF

---

## Design Philosophy

AI-KIP's visual language communicates **intelligence, precision, and trust**. The design follows four principles:

1. **Clarity over Decoration** -- Function before form
2. **Consistency creates Trust** -- Same patterns everywhere
3. **Accessibility by Default** -- WCAG 2.1 AA compliance
4. **Scalable Components** -- Build once, use everywhere

---

## Two Modes

| Context | Mode | When to use |
|---------|------|-------------|
| **Marketing / External** | Dark Mode | Carousels, social media, brochures, pitch decks, ads |
| **Product / Internal** | Light Mode | Web app, dashboards, documentation, internal emails |

Both modes share the same typography, spacing grid, and brand gradient. Only background and text color palettes shift.

**Important:** Never mix Dark and Light Mode within one document.

---

## Brand Gradient (Primary Identity)

```css
background: linear-gradient(90deg, #00FFFF, #FF00FF);
```

| Token | Hex | Role |
|-------|-----|------|
| **Accent Cyan** | `#00FFFF` | Gradient start, data highlights, interactive elements |
| **Accent Magenta** | `#FF00FF` | Gradient end, energy, urgency |

**Use for:** Logo text, labels, CTA buttons (background), flow lines, decorative accents, key stats.
**Never use for:** Body text or large background fills.

**Print/email fallback:** `#00CCCC` (Cyan) as flat color.

---

## Color Palette (Summary)

### Dark Mode -- Marketing

| Element | Hex | Usage |
|---------|-----|-------|
| Base Dark | `#0B0F1A` | Primary background |
| Deep Navy | `#141F40` | Mid-range backgrounds |
| Rich Indigo | `#242C62` | Later sections |
| Deep Purple | `#302F75` | Final section / CTA |
| Text Primary | `#F2F4F8` | Headlines, primary content |
| Text Secondary | `#C8CDD5` | Body text, descriptions |
| Text Muted | `#A0A7B5` | Sublines, secondary info |
| Bold/Emphasis | `#FFFFFF` | `<strong>` text within body |

**Background progression:** For multi-page materials (carousels, brochures), background gradually shifts from Base Dark to Deep Purple.

### Light Mode -- Product

| Element | Hex | Usage |
|---------|-----|-------|
| BG Base | `#F8F9FC` | Page background |
| Surface | `#FFFFFF` | Cards, sections |
| Text Primary | `#0B132B` | Headlines, body |
| Text Secondary | `#5F6B7A` | Descriptions, meta |
| Action Blue | `#2563EB` | Links, primary buttons |

### Additional Secondary Colors

| Color | Hex | Context |
|-------|-----|---------|
| Green | `#00ffb2` | Success, positive signals |
| Blue | `#47a6fc` | Information, links |
| Purple Blue | `#3c61ee` | Accents, highlights |
| Dark Purple | `#352257` | Deep backgrounds |

---

## Typography

| Font | Role | Source |
|------|------|--------|
| **Rubik** | Headlines, labels, logo text, buttons, display numbers | Google Fonts |
| **Inter** | Body text, sublines, captions, UI text | Google Fonts |

**Fallback stack:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

### Key Rules
- Never more than 2 font families (Rubik + Inter)
- Never below 400 or above 800 weight
- Headlines max 76px (never scale higher)
- Body text always left-aligned (never centered)
- No all-caps for body text

---

## Logo

| Element | Specification |
|---------|---------------|
| **File** | `logo.png` (transparent PNG) |
| **Icon size** | 72px height (marketing), 32-40px (product UI) |
| **Logo text** | "AI Knowledge & Interaction Platform" |
| **Logo font** | Rubik 700, gradient fill |
| **Gap** | 18px between icon and text |
| **Minimum clear space** | 1x icon height on all sides |

---

## Core Components

### Label with Underline
Category tag above a headline. Always uses brand gradient.
```
[Label Text -- 36px Rubik 700, Gradient]
[130px x 6px bar, Gradient, border-radius: 3px]
[32px gap]
[Headline]
```

### Quote Box
Left-bordered quote with gradient border for testimonials.

### Bullet Points
Arrow style (`->`) with cyan accent (`#00FFFF`).

### CTA Button
Gradient background, 16px border-radius, Rubik 700, dark text (`#0B0F1A`).

### Flow Line (Carousel)
6px gradient line as visual connection between slides.

---

## Format-Specific Sizes

| Format | Size | Note |
|--------|------|------|
| LinkedIn Carousel | 1080 x 1350px | 4:5 portrait, 8 slides optimal |
| LinkedIn Post | 1200 x 627px | Landscape, single message |
| Instagram Post | 1080 x 1080px | Square |
| Instagram Story | 1080 x 1920px | Vertical |
| HTML Email | 600px wide | Fluid to 320px minimum |
| A4 Brochure | ~794px base | 3mm bleed, 300 DPI |
| Slide Deck | 1920 x 1080px | 16:9 |

---

## Do's and Don'ts (Summary)

### Do
- Use Cyan-Magenta gradient only for accents and highlights
- Keep headlines short and punchy (2-4 lines max)
- Bold key phrases strategically (1-2 per paragraph)
- Maintain generous whitespace
- Include source citations for all statistics

### Don't
- Use gradient as full background fill
- Mix Dark and Light Mode in one document
- Place body text directly on the gradient
- Use colored body text
- Center-align body text

---

## Accessibility

- WCAG 2.1 AA conformance
- Keyboard navigable
- Animations: 150-300ms
- All images with alt text
- Retina-ready (2x) images
