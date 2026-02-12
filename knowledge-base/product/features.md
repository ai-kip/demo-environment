# Product Features -- What AI-KIP Can Do

> **Last updated:** 2026-02-09

---

## AI-KIP Sales Intelligence -- Feature Overview

### Data Foundation

| Feature | Detail |
|---------|--------|
| **Company database** | 33,000,000+ registered companies in Europe |
| **Decision maker database** | 850,000+ decision makers with roles and context |
| **Market signals** | 1,000,000+ daily signals |
| **Data sources** | Chamber of commerce, Dun & Bradstreet, Google Maps verified, trade registers -- everywhere a register exists |
| **Data collection** | AI agents scraping various systems worldwide via proxies |
| **Updates** | Reasoning models updated every 3 months |

### Core Features

#### 1. Lookalike Audience Generation
- Input: Domain or unique identifier of existing customers
- Output: Ideal customer profile (ICP) abstracted
- Filterable by industry, product-market fit, lifecycle
- Visualization of current vs. potential customers

#### 2. Signal Intelligence
- Real-time detection of buying signals from diverse sources
- Signal sources: LinkedIn, websites, forums, blogs, job postings, press releases, news coverage, annual reports, trade registers, and more
- Signal types:
  - Job postings / new hires
  - Annual reports / earnings
  - New locations / expansion plans
  - Factory permits / building permits
  - Leadership changes
  - Patent filings
  - Mergers and acquisitions
  - Funding rounds
  - Product discontinuations
  - Inventory surplus indicators
- Categorized as "Hot Opportunities" (immediate action) and "Strategic Opportunities" (monitoring)
- Confidence scores on each signal
- Competition level indicators (high/medium/low)

#### 3. Stakeholder Intelligence
- Identification of decision makers within companies
- Detection of hidden concerns in buying cycles
- Analysis of meeting transcripts (employee connects their own transcripts, retains control)

#### 4. CRM Data Quality
- Automatic cleansing and enrichment
- Identification of the entity behind company names
- Solves the "name correct, everything else garbage" problem

#### 5. MEDDPICC Scoring
- Automatic deal evaluation using the MEDDPICC framework
- Metrics, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Identify Pain, Champion, Competition

#### 6. Bowtie Pipeline Visualization
- 8-stage funnel visualization
- Go-to-market view: partner, end customer, indirect and direct motion
- Tracking through awareness, education, selection stages

#### 7. Outreach Sequences
- Multi-channel automated outreach campaigns
- Sequence management with status tracking (Active, Paused, Draft)
- Step-based workflows with enrollment tracking
- Reply rate monitoring and optimization
- Template library for quick sequence creation

#### 8. Thought Leadership / Meeting Prep
- AI-powered meeting preparation with automatic briefing generation
- Transcript indexing and insight extraction (1,247+ transcripts, 342+ insights)
- Knowledge base built from meeting history
- Calendar integration (Google Calendar, Outlook Calendar)
- Article generation from meeting insights
- Confidence-scored recommendations for upcoming meetings

#### 9. Deep Work (Human-in-the-Loop AI)
- AI agent signal classification with reasoning transparency
- Human validation workflow for agent decisions
- Session-based decision review (decisions this week, flagged for review, emerging patterns, learnings added)
- AI Assistant chat for real-time collaboration on signal interpretation
- Knowledge base learning entries that improve agent accuracy over time
- Confidence thresholds for automated vs. human-reviewed decisions

---

## Product UI Overview

The Sales Intelligence Platform has a dark-mode interface with the following main navigation:

| Screen | Purpose | Key Elements |
|--------|---------|--------------|
| **Dashboard** | Daily overview and prioritization | Bowtie pipeline visualization (AWR→EDU→SEL→COMMIT→ONB→ADP→EXP), Priority Deals, Today's Schedule, AI Recommendations with confidence scores |
| **Pipeline** | Funnel health and conversion tracking | Acquisition/Activation/Expansion metrics, stage-by-stage conversion rates, total accounts, pipeline value, at-risk and stalled deals |
| **Leads** | Lead management and prioritization | Card-based layout with status indicators (New, Contacted, Qualified), source tracking, urgency sorting, action buttons |
| **Deals** | Individual deal management | MEDDPICC radar chart and element scores (e.g., 64/80), deal value, stage, buying committee with roles, deal timeline |
| **Signals** | Buying signal intelligence | Hot Opportunities and Strategic Opportunities with confidence scores, signal categories, competition level indicators |
| **Deep Work** | Human-AI collaboration on decisions | Signal classification review, AI reasoning chains, human validation chat, knowledge base learning |
| **Sequences** | Outreach automation | Multi-channel sequence management, enrollment tracking, reply rate monitoring |
| **Thought Leadership** | Meeting prep and knowledge | Transcript indexing, insight extraction, briefing generation, calendar integration |
| **Analytics** | Performance reporting | (Available in navigation) |
| **Contacts** | Contact management | (Available in navigation) |
| **Intent** | Intent data tracking | (Available in navigation) |

> **Note for content creators:** The UI uses the dark mode design system (dark background, cyan/magenta accents). Screenshots are available at `SIP Screenshots/` folder. The interface is personalized (e.g., "Good morning, Daan") and shows real-time AI recommendations.

---

## Knowledge Interaction Platform (KIP) -- Feature Overview

### Platform Architecture

KIP is more than a single tool -- it can replace the entire software stack:

> "They kicked out all standard software... no ERP anymore, no CRM anymore."
> -- Aquablu case study

### Four Service Pillars

| Pillar | Description | Details |
|--------|-------------|---------|
| **Platform** | The enterprise intelligence layer where people and digital agents collaborate | Connects LLMs, agents, and data sources into a single backbone. Built on Lean, DevOps, and Kaizen principles. |
| **AI Professional Services** | Turning strategy into action through consulting and implementation | Opportunity identification, impact/feasibility assessment, implementation, adoption, monitoring. Full-scale programs to embed AI. |
| **AI Education** | Building the knowledge base for the workforce | E-learning courses, ebooks, articles, podcasts, newsletters, communities (LinkedIn, WhatsApp, Slack, Signal, Telegram). Structured programs and certifications. |
| **AI Talent** | Developing the next generation of leaders | Trainees, interns, young professionals from universities placed into organizations. Companies can also enroll their own talent. |

### AI Agent Progression Model

| Level | Type | Description | Key Features |
|-------|------|-------------|--------------|
| 1 | Rule-based Automation | Simple if-then rules, predetermined triggers | Deterministic actions, no learning capabilities |
| 2 | Intelligent Automation | Basic AI for semi-structured data, pattern recognition | Basic AI/ML models, error handling, basic analytics |
| 3 | Agentic Workflows | Foundation models with NLU, reasoning, orchestration | Advanced language understanding, short-term learning from feedback |
| 4 | Semi-Autonomous Agents | Multi-modal perception, autonomous task planning | Complex goal understanding, learning from past experiences, some human oversight |
| 5 | Fully Autonomous Agents | Full environmental awareness, independent goal formulation | Advanced reasoning, full autonomy, continuous learning and long-term adaptation |

### Operational Agent Levels (How agents execute within the platform)

| Level | Mode | Description |
|-------|------|-------------|
| 1 | Assisted | Intelligence supports humans: search, summarize, draft, explain |
| 2 | Automated | Repetitive tasks execute end-to-end: classifying tickets, routing requests |
| 3 | Adaptive | Systems learn from outcomes: recommendations improve, triage gets smarter |
| 4 | Collaborative | Multiple agents and humans coordinate: context shared across departments |
| 5 | Autonomous (with guardrails) | Agents manage bounded processes, self-monitor quality, escalate exceptions |

### Agentic AI -- How It Works

AI-KIP does **not** use generic LLMs (ChatGPT etc.), but specialized agent chains:

- 23+ different tasks that agents execute
- Agents request human reasoning to improve
- Human-AI collaboration, not full autonomy

> "95% of real world tasks given to AI are failing... because they used ChatGPT and other generic LLMs to do complex tasks."

---

## Technical Infrastructure

| Component | Technology |
|-----------|------------|
| **Frontend** | React 19 |
| **Backend** | FastAPI |
| **Graph Database** | Neo4j |
| **Vector Store** | Qdrant |
| **Cache** | Redis |
| **Object Storage** | MinIO |
| **Container** | Docker |
| **Hosting** | Schwarz IT / StackIT (Germany) |
| **Option** | On-premise installation at customer site |

---

## Pricing Model

| Element | Detail |
|---------|--------|
| **Model** | Monthly Recurring Revenue (MRR) |
| **Minimum contract** | 1 year |
| **MRR range** | EUR 2,500 -- 30,000 per month |
| **Depends on** | Use cases, usage volume, number of users |
| **Workshop** | EUR 2,500 for a 1-day onsite workshop (entry point) |

> **Pricing principle:** Communicated transparently and early. No "we'll send you a proposal" without prior discussion.

---

## Engagement Options

| Option | Description | Price |
|--------|-------------|-------|
| **Workshop** | 1-day onsite discovery: Use cases, ICP definition, automation mapping | EUR 2,500 |
| **Proof of Concept** | Demo with real customer data (50+ companies) | On request |
| **Full Service** | Complete implementation and ongoing support | MRR based |
| **Learning Session** | Introduction and orientation | On request |
| **Co-Development** | Joint development (only for selected strategic partners) | On request |

---

## Full Platform Replacement Potential

At maximum implementation, AI-KIP can replace:

- CRM (Customer Relationship Management)
- ERP (Enterprise Resource Planning)
- Traditional sales intelligence tools
- Individual AI point solutions

> **Important:** This is the maximum. Most customers start with Sales Intelligence as the entry point and expand step by step.
