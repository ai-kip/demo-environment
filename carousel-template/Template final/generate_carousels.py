"""
Generate all 6 AI-KIP LinkedIn Carousel HTML files and convert to PDF.
Uses the Template Final design specs.
"""
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR.parent / "Output final"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── CSS (identical to TEMPLATE-carousel-final.html) ──────────────────────────

CSS = """
@page { size: 1080px 1350px; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', sans-serif; }

.slide {
    width: 1080px; height: 1350px; position: relative;
    display: flex; flex-direction: column;
    page-break-after: always; page-break-inside: avoid; overflow: hidden;
}
.slide:last-child { page-break-after: auto; }

.slide-1 { background: linear-gradient(135deg, #0B0F1A 0%, #0D1220 30%, #0F1428 50%, #111833 70%, #0B1A2A 100%); }
.slide-1::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 10% 90%, rgba(0,255,255,.15) 0%, transparent 50%); pointer-events: none; }
.slide-2 { background: linear-gradient(135deg, #0B1A2A 0%, #0E1830 30%, #111D38 50%, #142040 70%, #0F1A35 100%); }
.slide-2::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 30% 70%, rgba(0,255,255,.12) 0%, transparent 50%); pointer-events: none; }
.slide-3 { background: linear-gradient(135deg, #0F1A35 0%, #121E3A 30%, #152242 50%, #18254A 70%, #141F40 100%); }
.slide-3::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 60%, rgba(71,166,252,.12) 0%, transparent 50%); pointer-events: none; }
.slide-4 { background: linear-gradient(135deg, #141F40 0%, #172345 30%, #1A264D 50%, #1D2955 70%, #192448 100%); }
.slide-4::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 70% 50%, rgba(60,97,238,.12) 0%, transparent 50%); pointer-events: none; }
.slide-5 { background: linear-gradient(135deg, #192448 0%, #1C2750 30%, #1F2A58 50%, #222D60 70%, #1E2855 100%); }
.slide-5::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 80% 40%, rgba(100,80,200,.12) 0%, transparent 50%); pointer-events: none; }
.slide-6 { background: linear-gradient(135deg, #1E2855 0%, #212B5D 30%, #252E65 50%, #29316D 70%, #242C62 100%); }
.slide-6::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 85% 35%, rgba(140,60,180,.12) 0%, transparent 50%); pointer-events: none; }
.slide-7 { background: linear-gradient(135deg, #242C62 0%, #282F6A 30%, #2C3272 50%, #30357A 70%, #2A3070 100%); }
.slide-7::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 90% 25%, rgba(180,50,200,.15) 0%, transparent 50%); pointer-events: none; }
.slide-8 { background: linear-gradient(135deg, #2A3070 0%, #2E3378 30%, #323680 50%, #363988 70%, #302F75 100%); }
.slide-8::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 95% 15%, rgba(255,0,255,.18) 0%, transparent 50%); pointer-events: none; }

.slide-header {
    height: 337px; padding: 50px 60px;
    display: flex; justify-content: space-between; align-items: flex-start;
    position: relative; z-index: 10;
}
.logo-container { display: flex; align-items: center; gap: 18px; }
.logo { height: 72px; width: auto; }
.logo-text {
    font-family: 'Rubik', sans-serif; font-weight: 700; font-size: 24px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.slide-number { font-family: 'Rubik', sans-serif; font-size: 32px; color: #00FFFF; font-weight: 600; }

.slide-content {
    height: 675px; padding: 0 80px;
    display: flex; flex-direction: column; justify-content: flex-start;
    position: relative; z-index: 10;
}
.label {
    font-family: 'Rubik', sans-serif; font-size: 36px; font-weight: 700;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 12px;
}
.label-underline {
    width: 130px; height: 6px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    border-radius: 3px; margin-bottom: 32px;
}
.headline {
    font-family: 'Rubik', sans-serif; font-weight: 700; color: #F2F4F8;
    line-height: 1.05; margin-bottom: 40px;
}
.headline-xl { font-size: 76px; }
.headline-lg { font-size: 62px; }
.headline-gradient {
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.subline { font-family: 'Inter', sans-serif; font-size: 44px; color: #A0A7B5; line-height: 1.4; }
.body-text {
    font-family: 'Inter', sans-serif; font-size: 38px; color: #C8CDD5;
    line-height: 1.5; margin-bottom: 24px;
}
.body-text strong { color: #FFFFFF; font-weight: 600; }
.quote {
    font-family: 'Inter', sans-serif; font-size: 36px; color: #C8CDD5;
    font-style: italic; padding-left: 36px;
    border-left: 6px solid; border-image: linear-gradient(180deg, #00FFFF, #FF00FF) 1;
    margin: 24px 0; line-height: 1.45;
}
.source { font-family: 'Inter', sans-serif; font-size: 26px; color: #7A8290; margin-top: 16px; }
.bullets { list-style: none; padding: 0; margin: 24px 0; }
.bullets li {
    font-family: 'Inter', sans-serif; font-size: 36px; color: #C8CDD5;
    padding-left: 48px; position: relative; margin-bottom: 20px; line-height: 1.45;
}
.bullets li::before {
    content: '\\2192'; position: absolute; left: 0; color: #00FFFF; font-weight: bold; font-size: 38px;
}
.cta-button {
    display: inline-block; padding: 24px 48px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
    border-radius: 16px; font-family: 'Rubik', sans-serif;
    font-size: 28px; color: #0B0F1A; font-weight: 700; margin-top: 32px;
}

.slide-footer-area { height: 338px; position: relative; z-index: 10; }
.flow-line {
    position: absolute; top: 120px; left: 0; right: 0; height: 6px;
    background: linear-gradient(90deg, #00FFFF, #FF00FF);
}
.slide-1 .flow-line { left: 50%; border-radius: 3px 0 0 3px; }
.slide-1 .flow-line::before {
    content: ''; position: absolute; left: 0; top: 50%; transform: translate(-50%,-50%);
    width: 26px; height: 26px; background: #00FFFF; border-radius: 50%;
    box-shadow: 0 0 24px #00FFFF, 0 0 48px #00FFFF;
}
.slide-8 .flow-line { right: 50%; left: 0; border-radius: 0 3px 3px 0; }
.slide-8 .flow-line::after {
    content: ''; position: absolute; right: 0; top: 50%; transform: translate(50%,-50%);
    width: 26px; height: 26px; background: #FF00FF; border-radius: 50%;
    box-shadow: 0 0 24px #FF00FF, 0 0 48px #FF00FF;
}
.slide-footer {
    position: absolute; bottom: 50px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center;
}
.swipe-hint { font-family: 'Inter', sans-serif; font-size: 28px; color: #6A7080; }
.swipe-hint span { color: #00FFFF; margin-left: 12px; }
.website { font-family: 'Inter', sans-serif; font-size: 32px; color: #8A90A0; font-weight: 500; }
"""

# ── HTML generators ──────────────────────────────────────────────────────────

def html_header(slide_num):
    return f"""        <div class="slide-header">
            <div class="logo-container">
                <img src="logo.png" alt="AI-KIP" class="logo">
                <span class="logo-text">AI Knowledge &amp; Interaction Platform</span>
            </div>
            <span class="slide-number">{slide_num}/8</span>
        </div>"""


def html_footer_swipe():
    return """        <div class="slide-footer-area">
            <div class="flow-line"></div>
            <div class="slide-footer">
                <span class="swipe-hint">Swipe <span>&rarr;</span></span>
            </div>
        </div>"""


def html_footer_website(url="ai-kip.com"):
    return f"""        <div class="slide-footer-area">
            <div class="flow-line"></div>
            <div class="slide-footer">
                <span class="website">{url}</span>
            </div>
        </div>"""


def render_body(items):
    """Render body items list into HTML.
    Each item is one of:
      str                           -> <p class="body-text">...</p>
      ("bullets", [str, ...])       -> <ul class="bullets">...</ul>
      ("quote", str)                -> <p class="quote">...</p>
      ("source", str)               -> <p class="source">...</p>
    """
    parts = []
    for item in items:
        if isinstance(item, str):
            parts.append(f'            <p class="body-text">{item}</p>')
        elif isinstance(item, tuple):
            kind = item[0]
            if kind == "bullets":
                lis = "\n".join(f"                <li>{b}</li>" for b in item[1])
                parts.append(f'            <ul class="bullets">\n{lis}\n            </ul>')
            elif kind == "quote":
                parts.append(f'            <p class="quote">{item[1]}</p>')
            elif kind == "source":
                parts.append(f'            <p class="source">{item[1]}</p>')
    return "\n".join(parts)


def build_slide(num, slide):
    t = slide["type"]
    cls = f"slide slide-{num}"
    lines = [f'    <div class="{cls}">']
    lines.append(html_header(num))

    lines.append('        <div class="slide-content">')

    if t == "hook":
        grad = " headline-gradient" if slide.get("gradient", True) else ""
        lines.append(f'            <h1 class="headline headline-xl{grad}">{slide["headline"]}</h1>')
        if slide.get("subline"):
            lines.append(f'            <p class="subline">{slide["subline"]}</p>')

    elif t == "content":
        lines.append(f'            <span class="label">{slide["label"]}</span>')
        lines.append('            <div class="label-underline"></div>')
        grad = " headline-gradient" if slide.get("gradient", False) else ""
        size = slide.get("size", "lg")
        lines.append(f'            <h2 class="headline headline-{size}{grad}">{slide["headline"]}</h2>')
        lines.append(render_body(slide["body"]))

    elif t == "cta":
        lines.append(f'            <h2 class="headline headline-xl">{slide["headline"]}</h2>')
        lines.append(render_body(slide["body"]))
        lines.append(f'            <span class="cta-button">{slide["cta_text"]}</span>')

    lines.append('        </div>')

    if t == "cta" and slide.get("website"):
        lines.append(html_footer_website(slide["website"]))
    elif num == 8:
        lines.append(html_footer_website())
    else:
        lines.append(html_footer_swipe())

    lines.append('    </div>')
    return "\n".join(lines)


def build_carousel_html(title, slides):
    slide_html = "\n\n".join(build_slide(i + 1, s) for i, s in enumerate(slides))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Rubik:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>{CSS}
    </style>
</head>
<body>

{slide_html}

</body>
</html>
"""


# ── CAROUSEL CONTENT ─────────────────────────────────────────────────────────

CAROUSELS = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CAROUSEL 1: THE AI OPPORTUNITY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "num": 1,
        "slug": "ai-opportunity",
        "title": "AI-KIP – The AI Opportunity",
        "slides": [
            {
                "type": "hook",
                "headline": "95% of AI Projects<br>Fail to Deliver<br>ROI.",
                "subline": "Here's Why Yours Might Be Next",
            },
            {
                "type": "content",
                "label": "A Common Situation",
                "headline": "More Dashboards,<br>Same Results",
                "body": [
                    "The average B2B sales team uses <strong>10+ tools</strong>, yet reps still spend most of their day researching instead of selling.",
                ],
            },
            {
                "type": "content",
                "label": "The Insight",
                "headline": "Generic AI Is Only<br>Step One in<br>B2B Sales",
                "body": [
                    "ChatGPT can write emails.",
                    "But it can't tell you <strong>which of your prospects is ready to buy</strong> this quarter.",
                ],
            },
            {
                "type": "content",
                "label": "The Real Opportunity",
                "headline": "70% of Sales Time<br>Is Non-Selling",
                "body": [
                    "Lead research, CRM updates, list building, and admin still consume most of a rep's week.",
                    "<strong>Automating this unlocks massive upside.</strong>",
                    ("source", "— Salesforce State of Sales Report (2024)"),
                ],
            },
            {
                "type": "content",
                "label": "What You Need",
                "headline": "Answers, Not<br>More Data",
                "body": [
                    ("bullets", [
                        "Who should I call today?",
                        "Why is this account relevant now?",
                        "What's the best angle to use?",
                    ]),
                    "That's where AI creates <strong>ROI</strong>.",
                ],
            },
            {
                "type": "content",
                "label": "The Performance Gap",
                "headline": "3\u00d7 Higher ROI with<br>Orchestrated Agents",
                "body": [
                    "Companies using orchestrated AI agents see <strong>3x higher ROI</strong> than those using standalone AI tools.",
                    ("source", "— BCG \u201cThe Agentic AI Playbook\u201d (2025)"),
                ],
            },
            {
                "type": "content",
                "label": "The Impact",
                "headline": "Up to 20%<br>More Revenue",
                "body": [
                    "AI-powered pipeline optimization drives <strong>up to 20% revenue increase</strong> in B2B sales.",
                    "That's not hype \u2014 that's McKinsey data.",
                    ("source", "— McKinsey \u201cThe state of AI in early 2025\u201d"),
                ],
            },
            {
                "type": "cta",
                "headline": "AI Should Create<br>Leverage.",
                "body": [
                    "Not more <strong>complexity</strong>.",
                ],
                "cta_text": "Follow for More Insights",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CAROUSEL 2: 4 TIME OPPORTUNITIES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "num": 2,
        "slug": "time-opportunities",
        "title": "AI-KIP – 4 Hidden Drains on Your Pipeline",
        "slides": [
            {
                "type": "hook",
                "headline": "4 Hidden Drains<br>on Your Pipeline",
                "subline": "(And Where the Biggest Gains Are)",
            },
            {
                "type": "content",
                "label": "Opportunity #1",
                "headline": "Research at Scale",
                "body": [
                    "Sales reps spend <strong>70% of their time</strong> on non-selling tasks.",
                    "Automating research instantly <strong>increases selling capacity</strong>.",
                    ("source", "— Salesforce State of Sales Report (2024)"),
                ],
            },
            {
                "type": "content",
                "label": "Opportunity #2",
                "headline": "Focus on the<br>Active 5%",
                "body": [
                    "Only <strong>5%</strong> of your total addressable market is actively buying at any given moment.",
                    "<strong>Precision beats volume.</strong>",
                    ("source", "— Ehrenberg-Bass Institute &amp; LinkedIn B2B Institute"),
                ],
            },
            {
                "type": "content",
                "label": "Opportunity #3",
                "headline": "Fix Your CRM<br>Data Decay",
                "body": [
                    "B2B contact data decays at <strong>22\u201330% per year</strong>.",
                    "That means nearly a third of your database becomes obsolete annually.",
                    ("source", "— HubSpot Database Decay Study"),
                ],
            },
            {
                "type": "content",
                "label": "Opportunity #4",
                "headline": "Win Earlier",
                "body": [
                    "<strong>70\u201380%</strong> of the buyer journey happens before first sales contact, and <strong>81%</strong> already have a preferred vendor by then.",
                    ("source", "— Gartner B2B Buying Journey; 6sense Buyer Experience Report (2024)"),
                ],
            },
            {
                "type": "content",
                "label": "The Pattern",
                "headline": "Effort Isn't<br>the Problem",
                "body": [
                    "Sales teams work hard.",
                    "Teams with <strong>real-time market signals</strong> work ahead of the buyer.",
                ],
            },
            {
                "type": "content",
                "label": "The Fix",
                "headline": "Intelligence<br>Before Action",
                "body": [
                    "Know which accounts are moving. Know why. Know when.",
                    "<strong>Then act</strong> \u2014 before your competition does.",
                ],
            },
            {
                "type": "cta",
                "headline": "Turn Insight<br>into Advantage.",
                "body": [
                    "Your team deserves <strong>leverage</strong>.",
                ],
                "cta_text": "Follow for Sales Tips",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CAROUSEL 3: THE 95:5 RULE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "num": 3,
        "slug": "95-5-rule",
        "title": "AI-KIP – The 95:5 Rule",
        "slides": [
            {
                "type": "hook",
                "headline": "The 95:5 Rule",
                "subline": "Why Timing Beats Volume in B2B",
            },
            {
                "type": "content",
                "label": "The Reality",
                "headline": "Only 5% Want to<br>Talk Right Now",
                "body": [
                    "At any given time, <strong>95%</strong> of your target market isn't ready to buy.",
                    "They're not ignoring you \u2014 they're simply <strong>not in-market yet</strong>.",
                    ("source", "— Ehrenberg-Bass Institute &amp; LinkedIn B2B Institute"),
                ],
            },
            {
                "type": "content",
                "label": "The Math",
                "headline": "Companies Change<br>Providers Every<br>5 Years",
                "body": [
                    "That means only <strong>20%</strong> are in-market per year \u2014 and just <strong>5% per quarter</strong> are active buyers.",
                    ("source", '— LinkedIn B2B Institute \u201cHow B2B Brands Grow\u201d'),
                ],
            },
            {
                "type": "content",
                "label": "The Cost of Treating Everyone Equally",
                "headline": "CAC Is Up<br>Over 50%",
                "body": [
                    "Same emails. Same cadence. Same pitch.",
                    "No wonder response rates keep dropping while costs keep rising. <strong>Over 50% increase</strong> in B2B customer acquisition costs.",
                    ("source", "— ProfitWell/Paddle B2B CAC Study"),
                ],
            },
            {
                "type": "content",
                "label": "The Signals",
                "headline": "How to Spot<br>the Active 5%",
                "body": [
                    "Hiring patterns. Tech stack changes. Funding rounds. Leadership moves. Press mentions.",
                    "These reveal <strong>who's ready to buy now</strong>.",
                ],
            },
            {
                "type": "content",
                "label": "The Winning Strategy",
                "headline": "Two Tracks,<br>One Goal",
                "body": [
                    "Nurture the 95% with <strong>brand building</strong> and content.",
                    "Activate the 5% with <strong>hyper-personalized outreach</strong>.",
                    "Different goals, different tactics.",
                ],
            },
            {
                "type": "content",
                "label": "The Payoff",
                "headline": "80% Win Rate for<br>Early Favorites",
                "body": [
                    "Vendors ranked first before buyers contact sales win <strong>80% of deals</strong>.",
                    ("source", "— 6sense Buyer Experience Report (2025)"),
                ],
            },
            {
                "type": "cta",
                "headline": "Stop Guessing.<br>Start Knowing.",
                "body": [
                    "Know exactly who the <strong>5%</strong> is.",
                ],
                "cta_text": "Follow for B2B Insights",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CAROUSEL 4: SCALING WITHOUT LIMITS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "num": 4,
        "slug": "scaling",
        "title": "AI-KIP – Scaling Without Limits",
        "slides": [
            {
                "type": "hook",
                "headline": "What If a 2-Person<br>Team Could<br>Outperform<br>a Team of 10?",
                "subline": "The New Math of AI-Powered Sales",
            },
            {
                "type": "content",
                "label": "The Ceiling",
                "headline": "Growth Hits a Wall",
                "body": [
                    "More accounts means more research. New markets need more reps.",
                    "<strong>Traditional scaling is a headcount problem.</strong>",
                ],
            },
            {
                "type": "content",
                "label": "The Reality",
                "headline": "Reclaim 70% of<br>Sales Time",
                "body": [
                    "Research and admin time frees your most expensive talent to focus on <strong>closing</strong>.",
                    ("source", "— Salesforce State of Sales Report (2024)"),
                ],
            },
            {
                "type": "content",
                "label": "The Possibility",
                "headline": "5\u00d7 Market<br>Coverage",
                "body": [
                    "A 2-person team with AI-KIP's platform can achieve the <strong>same market depth and quality</strong> as a 10-person team \u2014 at least.",
                ],
            },
            {
                "type": "content",
                "label": "How It Works",
                "headline": "AI-KIP Monitors<br>Your Entire Market",
                "body": [
                    "We track <strong>90,000+ companies</strong> and <strong>850,000+ decision-makers</strong>.",
                    "Over <strong>1 million market signals</strong> analyzed in real-time.",
                ],
            },
            {
                "type": "content",
                "label": "Customer Results",
                "headline": "300% Sales<br>Increase",
                "body": [
                    "Clients achieved a <strong>300% increase in sales</strong> within weeks of implementing AI-KIP's Sales Intelligence platform.",
                    ("source", "— AI-KIP Project Reference"),
                ],
            },
            {
                "type": "content",
                "label": "Built for You",
                "headline": "European B2B,<br>GDPR-Ready",
                "body": [
                    "<strong>100% GDPR/DSGVO-compliant.</strong>",
                    "Multi-language. Flexible hosting (local, private cloud). Understands how business works here.",
                ],
            },
            {
                "type": "cta",
                "headline": "Scale Without<br>the Headcount.",
                "body": [
                    "See what's possible for your team.",
                ],
                "cta_text": "Book a Demo",
                "website": "www.ai-kip.com",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CAROUSEL 5: THE PERFECT OUTREACH MESSAGE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "num": 5,
        "slug": "outreach",
        "title": "AI-KIP – The Perfect Outreach Message",
        "slides": [
            {
                "type": "hook",
                "headline": "B2B Buyers<br>Expect 80%<br>Personalization",
                "subline": "Here's How to Actually Deliver It",
            },
            {
                "type": "content",
                "label": "Element #1",
                "headline": "A Real Trigger",
                "body": [
                    ("quote", "\u201cI saw your company just announced expansion into France\u2026\u201d"),
                    "Reference something real: <strong>funding, hiring, leadership change</strong>. Show you actually looked.",
                ],
            },
            {
                "type": "content",
                "label": "Element #2",
                "headline": "Their Actual<br>Problem",
                "body": [
                    "<strong>Specific challenges</strong> outperform generic pain points every time.",
                    "Research beats templates.",
                ],
            },
            {
                "type": "content",
                "label": "Element #3",
                "headline": "Proof That Matters",
                "body": [
                    "One relevant case study beats a feature list.",
                    "<strong>Make it relatable.</strong>",
                ],
            },
            {
                "type": "content",
                "label": "Element #4",
                "headline": "Clear, Specific<br>Value",
                "body": [
                    ("\u201cSave 6 hours weekly on research\u201d hits harder than "
                     "\u201cimprove sales efficiency.\u201d"),
                    "<strong>Numbers beat adjectives.</strong>",
                ],
            },
            {
                "type": "content",
                "label": "Element #5",
                "headline": "One Simple Ask",
                "body": [
                    ("quote", "\u201cWorth a 15-min chat Thursday?\u201d"),
                    'Not \u201cI\'d love to schedule a call to discuss potential synergies.\u201d',
                ],
            },
            {
                "type": "content",
                "label": "The Problem",
                "headline": "Manual Research<br>Doesn't Scale",
                "body": [
                    "You can't hyper-personalize at volume with manual work.",
                    "Sales teams face a choice: <strong>generic mass outreach or quality that doesn't scale</strong>.",
                ],
            },
            {
                "type": "cta",
                "headline": "The Solution:<br>AI-Powered<br>Personalization",
                "body": [
                    "Let AI do the research. <strong>You do the relationship.</strong>",
                ],
                "cta_text": "Follow for Sales Tips",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # CAROUSEL 6: THE ROI OF SALES INTELLIGENCE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {
        "num": 6,
        "slug": "roi",
        "title": "AI-KIP – The ROI of Sales Intelligence",
        "slides": [
            {
                "type": "hook",
                "headline": "Your Reps Cost<br>EUR 80K/Year",
                "subline": "How Much of That Is Wasted on Research?",
            },
            {
                "type": "content",
                "label": "The Hidden Cost",
                "headline": "70% on Non-Selling<br>Activities",
                "body": [
                    "If 70% of your EUR 80K rep's time goes to admin tasks, that's <strong>EUR 56K/year per rep</strong> not spent on closing deals.",
                    ("source", "— Salesforce State of Sales Report (2024)"),
                ],
            },
            {
                "type": "content",
                "label": "The Multiplier",
                "headline": "Wrong Leads =<br>Compounded Loss",
                "body": [
                    "Only <strong>5%</strong> of prospects are in-market.",
                    "Every hour on the other 95% is an hour <strong>not spent on real opportunities</strong>.",
                    ("source", "— Ehrenberg-Bass Institute 95:5 Rule"),
                ],
            },
            {
                "type": "content",
                "label": "The Benchmark",
                "headline": "B2B Acquisition<br>Costs Are Rising",
                "body": [
                    "Customer acquisition costs have increased <strong>over 50%</strong>.",
                    "Efficiency is no longer optional \u2014 it's the <strong>growth lever</strong>.",
                    ("source", "— ProfitWell/Paddle B2B CAC Study"),
                ],
            },
            {
                "type": "content",
                "label": "The Alternative",
                "headline": "Cut Research<br>by Up to 70%",
                "body": [
                    "AI-KIP monitors your market <strong>24/7</strong>.",
                    "Surfaces buying signals. Delivers ready-to-use insights. Your team focuses on <strong>selling</strong>.",
                ],
            },
            {
                "type": "content",
                "label": "The Proof",
                "headline": "300% Sales<br>Increase",
                "body": [
                    ("quote", "Since implementing AI-KIP's Sales Intelligence Platform, we significantly increased qualified meetings within weeks, leading to a <strong>300% increase in sales</strong>."),
                    ("source", "— VP GTM, AI-KIP Client"),
                ],
            },
            {
                "type": "content",
                "label": "The Outcome",
                "headline": "Up to 20%<br>Revenue Growth",
                "body": [
                    "AI-powered pipeline optimization delivers <strong>up to 20% revenue increase</strong> in B2B sales.",
                    ("source", '— McKinsey \u201cThe state of AI in early 2025\u201d'),
                ],
            },
            {
                "type": "cta",
                "headline": "Calculate<br>Your ROI.",
                "body": [
                    "See what AI-KIP could mean for <strong>your numbers</strong>.",
                ],
                "cta_text": "Book a Demo",
                "website": "www.ai-kip.com",
            },
        ],
    },
]


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    html_files = []

    # 1) Generate HTML files
    for c in CAROUSELS:
        filename = f"carousel-{c['num']}-{c['slug']}.html"
        filepath = SCRIPT_DIR / filename
        html = build_carousel_html(c["title"], c["slides"])
        filepath.write_text(html, encoding="utf-8")
        html_files.append(filepath)
        print(f"[HTML] {filename}")

    # 2) Convert each to PDF via convert.py
    convert_script = SCRIPT_DIR / "convert.py"
    for html_file in html_files:
        pdf_name = html_file.stem + ".pdf"
        pdf_path = OUTPUT_DIR / pdf_name
        print(f"\n{'='*60}")
        print(f"Converting {html_file.name} -> {pdf_name}")
        print(f"{'='*60}")

        ret = os.system(
            f'python "{convert_script}" "{html_file}" "{pdf_path}"'
        )
        if ret != 0:
            print(f"ERROR converting {html_file.name}")

    # 3) Clean up temp HTML files
    for f in html_files:
        f.unlink(missing_ok=True)
        print(f"[CLEANUP] Removed {f.name}")

    print(f"\nDone! PDFs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
