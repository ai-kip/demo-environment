# AI-KIP LinkedIn Carousel Design Template

## Format

| Eigenschaft | Wert |
|-------------|------|
| **Breite** | 1080px |
| **Höhe** | 1350px |
| **Seitenverhältnis** | 4:5 (Portrait) |
| **Dateiformat** | PDF |

---

## Layout-Struktur (Vierteilung)

```
┌─────────────────────────────────────┐  ─┐
│                                     │   │
│  [Logo] AI-KIP              1/8     │   │ VIERTEL 1
│                                     │   │ Header (337px)
│                                     │   │
├─────────────────────────────────────┤  ─┤
│                                     │   │
│  Label                              │   │
│  ────────                           │   │
│                                     │   │ VIERTEL 2+3
│  HEADLINE                           │   │ Content (675px)
│                                     │   │
│  Body Text                          │   │
│  Body Text                          │   │
│                                     │   │
├─────────────────────────────────────┤  ─┤
│                                     │   │
│  ════════════════════════════════   │   │ VIERTEL 4
│                                     │   │ Footer (338px)
│  Weiter →                           │   │
│                                     │   │
└─────────────────────────────────────┘  ─┘
```

### Bereichshöhen

| Bereich | Höhe | Padding |
|---------|------|---------|
| **Header** | 337px | 50px oben, 60px links/rechts |
| **Content** | 675px | 80px links/rechts |
| **Footer** | 338px | Flow-Line bei 120px von oben |

---

## Farbpalette (Dark Mode)

### Hintergrund-Gradient (verläuft über alle 8 Slides)

| Slide | Primärfarbe | Glow-Position | Glow-Farbe |
|-------|-------------|---------------|------------|
| 1 | #0B0F1A → #0B1A2A | 10% 90% | Cyan (15%) |
| 2 | #0B1A2A → #0F1A35 | 30% 70% | Cyan (12%) |
| 3 | #0F1A35 → #141F40 | 50% 60% | Blau (12%) |
| 4 | #141F40 → #192448 | 70% 50% | Purple-Blue (12%) |
| 5 | #192448 → #1E2855 | 80% 40% | Lila (12%) |
| 6 | #1E2855 → #242C62 | 85% 35% | Lila (12%) |
| 7 | #242C62 → #2A3070 | 90% 25% | Magenta (15%) |
| 8 | #2A3070 → #302F75 | 95% 15% | Magenta (18%) |

### Text-Farben

| Element | Hex | Verwendung |
|---------|-----|------------|
| **Text Primary** | #F2F4F8 | Headlines |
| **Text Secondary** | #C8CDD5 | Body-Text |
| **Text Muted** | #A0A7B5 | Sublines |
| **Text Subtle** | #7A8290 | Source-Angaben |
| **Text Footer** | #6A7080 | "Weiter" Hinweis |
| **Accent Cyan** | #00FFFF | Slide-Nummer, Pfeile |
| **Accent Magenta** | #FF00FF | Gradient-Ende |

### Gradient (Brand)

```css
background: linear-gradient(90deg, #00FFFF, #FF00FF);
```

Verwendung: Logo-Text, Labels, Headlines (optional), Flow-Line, CTA-Button

---

## Typografie

### Schriftarten

| Font | Verwendung |
|------|------------|
| **Rubik** | Headlines, Labels, Logo-Text, Buttons |
| **Inter** | Body-Text, Sublines, Footer |

### Schriftgrößen

| Element | Font | Größe | Gewicht | Farbe |
|---------|------|-------|---------|-------|
| **Logo-Text** | Rubik | 36px | 700 | Gradient |
| **Slide-Nummer** | Rubik | 32px | 600 | #00FFFF |
| **Label** | Rubik | 36px | 700 | Gradient |
| **Headline XL** | Rubik | 76px | 700 | #F2F4F8 oder Gradient |
| **Headline LG** | Rubik | 62px | 700 | #F2F4F8 |
| **Subline** | Inter | 44px | 400 | #A0A7B5 |
| **Body-Text** | Inter | 38px | 400 | #C8CDD5 |
| **Quote** | Inter | 36px | 400 italic | #C8CDD5 |
| **Bullets** | Inter | 36px | 400 | #C8CDD5 |
| **Source** | Inter | 26px | 400 | #7A8290 |
| **Swipe-Hint** | Inter | 28px | 400 | #6A7080 |
| **Website** | Inter | 32px | 500 | #8A90A0 |
| **CTA-Button** | Rubik | 28px | 700 | #0B0F1A |

---

## Komponenten

### Logo-Container

```
[Logo-Icon 72px] + [16px Gap] + [AI-KIP Text 36px Gradient]
```

Position: Oben links im Header

### Label mit Underline

```
Label-Text (36px, Gradient)
────────── (130px breit, 6px hoch, Gradient)
[32px Abstand]
```

### Quote-Box

```css
border-left: 6px solid;
border-image: linear-gradient(180deg, #00FFFF, #FF00FF) 1;
padding-left: 36px;
```

### Bullet-Points

```
→ Text (Pfeil in #00FFFF, 48px padding-left)
```

### CTA-Button

```css
padding: 24px 48px;
background: linear-gradient(90deg, #00FFFF, #FF00FF);
border-radius: 16px;
color: #0B0F1A;
```

### Flow-Line

```css
height: 6px;
background: linear-gradient(90deg, #00FFFF, #FF00FF);
```

- **Slide 1:** Startet bei 50%, Cyan-Dot (26px) mit Glow links
- **Slide 2-7:** Durchgehend von links nach rechts
- **Slide 8:** Endet bei 50%, Magenta-Dot (26px) mit Glow rechts

---

## Slide-Typen

### 1. Hook-Slide (Slide 1)

- Keine Label
- Headline XL mit Gradient
- Subline darunter
- Flow-Line startet

### 2. Content-Slides (Slide 2-7)

- Label + Underline
- Headline LG
- Body-Text (mehrere Absätze)
- Optional: Quote, Bullets, Source
- Flow-Line durchgehend

### 3. CTA-Slide (Slide 8)

- Keine Label
- Headline XL
- Body-Text mit CTA
- CTA-Button
- Flow-Line endet
- Website statt "Weiter"

---

## Dateien

```
C:\Users\mamowi\Clients\AI-KIP\carousel-template\
├── TEMPLATE-carousel.html    ← Master-Template (HTML)
├── TEMPLATE-carousel.pdf     ← Beispiel-Export (PDF)
├── TEMPLATE-SPECS.md         ← Diese Dokumentation
└── logo.png                  ← AI-KIP Logo
```

---

## Verwendung

1. `TEMPLATE-carousel.html` kopieren
2. Texte anpassen
3. In Browser öffnen → Print → PDF speichern
4. Oder mit Edge Headless:

```powershell
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --headless --disable-gpu --no-pdf-header-footer --print-to-pdf='output.pdf' 'file:///pfad/zur/datei.html'
```

---

## Version

- **Template-Version:** 1.0
- **Erstellt:** 05.02.2026
- **Basiert auf:** AI-KIP Style Guide (Dark Mode)
