# Vantage Point — AI-Native Intelligence Hub for Decision Makers


Vantage Point is a **multi-agent AI system** that acts as an autonomous Chief of Staff. It monitors Gmail, Google Calendar, Google Sheets, and an internal OKR database to detect risks, score goal progress, and deliver prioritized intelligence briefs — powered by **Google Gemini 2.5 Flash**.

Instead of manually checking emails, spreadsheets, and calendars every morning, a founder or VC opens Vantage Point and gets one synthesized brief: what's on fire, what's off track, and what to do about it.

---

## Problem Statement

> Build a multi-agent AI system that helps users manage tasks, schedules, and information
> by interacting with multiple tools and data sources.

---

## Architecture

```
                        ┌─────────────────────────┐
                        │   React Dashboard (UI)  │
                        │                         │
                        └───────────┬─────────────┘
                                    │ REST API
                        ┌───────────▼─────────────┐
                        │    FastAPI (main.py)    │
                        │    API Layer + CORS     │
                        └───────────┬─────────────┘
                                    │
                  ┌─────────────────▼──────────────────┐
                  │    Command Center (Orchestrator)   │
                  │    Plans → Delegates → Assembles   │
                  └──┬─────────┬──────────┬──────────┬─┘
                     │         │          │          │
            ┌────────┘    ┌────┘     ┌────┘     ┌────┘
            ▼             ▼          ▼          ▼
     Market Signal   Performance   Asset      Senior
       Agent          Auditor    Guardian   Synthesizer
     (Gmail MCP)   (Sheets MCP) (Cal MCP)  (Gemini 2.5)
            │             │          │          │
            └─────────────┴──────────┘          │
                     │                          │
              ┌──────▼──────┐           ┌───────▼───────┐
              │ MCP Servers │           │  Google       │
              │  (FastMCP)  │           │  Gemini API   │
              └──────┬──────┘           └───────────────┘
                     │
              ┌──────▼──────┐
              │  SQLite DB  │
              │ (Persistent │
              │   Storage)  │
              └─────────────┘
```

### Data Flow

1. **User triggers synthesis** via the dashboard ("Synthesize Intelligence" button or natural language query)
2. **Command Center** dispatches 3 data-ingestion agents in parallel using `asyncio.gather`
3. **Market Signal Agent** scans Gmail via MCP for client risks, blockers, unanswered threads
4. **Performance Auditor** reads OKR data from the database (extensible to Google Sheets via MCP)
5. **Asset Guardian** cross-references Google Calendar events with OKR deadlines to detect scheduling conflicts
6. All agent outputs are **consolidated** and passed to the **Senior Synthesizer**
7. **Gemini 2.5 Flash** generates a structured **Intelligence Brief** with prioritized risks and action items
8. The brief is **persisted** in SQLite and **rendered** on the React dashboard in real-time

---

## Core Requirements Coverage

| Hackathon Requirement | Our Implementation |
|---|---|
| **Primary agent coordinating sub-agents** | `Command Center (Orchestrator)` dispatches 4 sub-agents in parallel via asyncio |
| **Structured database** | SQLite via SQLAlchemy — OKRs, Signals, Risks, Briefs, Proactive Alerts |
| **Multiple MCP tools** | 3 FastMCP servers: Gmail, Google Calendar, Google Drive |
| **Multi-step workflows** | Signal detection → OKR scoring → Risk analysis → Gemini synthesis → Brief persistence |
| **API-based deployment** | FastAPI with 10+ REST endpoints, Dockerized for Cloud Run |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Gemini 2.5 Flash (via `google-genai` SDK) |
| **Backend** | FastAPI + Python 3.12 |
| **Frontend** | React 19 + Vite |
| **Database** | SQLite + SQLAlchemy ORM |
| **MCP** | FastMCP (Model Context Protocol) servers |
| **Design System** | "Lumina Ether" — glassmorphism, aurora gradients, editorial typography |
| **Deployment** | Docker → Google Cloud Run |

---

## Project Structure

```
vantage-point/
├── agents/
│   ├── orchestrator.py      # Command Center — primary coordinating agent
│   ├── signal_watcher.py    # Market Signal Agent — Gmail intelligence
│   ├── okr_tracker.py       # Performance Auditor — OKR scoring
│   ├── risk_spotter.py      # Asset Guardian — risk & calendar analysis
│   ├── advisor.py           # Senior Synthesizer — Gemini 2.5 Flash
│   └── scheduler.py         # Proactive health monitoring & alerting
├── db/
│   ├── models.py            # SQLAlchemy ORM models (OKR, Signal, Risk, Brief, Alert)
│   └── database.py          # DB engine, session management
├── tools/
│   ├── mcp_client.py        # MCP tool abstraction layer
│   └── simulate_crisis.py   # Live demo crisis injection tool
├── mcp_servers/
│   ├── gmail_server.py      # FastMCP Gmail server
│   ├── calendar_server.py   # FastMCP Calendar server
│   └── drive_server.py      # FastMCP Drive server
├── frontend/
│   ├── src/
│   │   ├── views/           # Dashboard, Strategy Hub, Risk Deep-Dive
│   │   ├── components/      # TopNav, HealthOrb, StatsRow, CommandBar, etc.
│   │   ├── App.jsx          # Router + global state management
│   │   ├── api.js           # Backend API client
│   │   └── index.css        # Lumina Ether design system
│   └── ...
├── data/
│   └── seed.py              # Realistic demo data seeder
├── main.py                  # FastAPI entry point (10+ endpoints)
├── Dockerfile               # Multi-stage production build
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/BalajiReddy1/Vantage-Point.git
cd Vantage-Point

# Python dependencies
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Frontend dependencies
cd frontend && npm install && cd ..
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```

### 3. Seed Demo Data

```bash
python -m data.seed
```

### 4. Run Backend

```bash
uvicorn main:app --host 127.0.0.1 --port 8001
```

### 5. Run Frontend (Development)

```bash
cd frontend
npm run dev
```

### 6. Open Dashboard

Navigate to `http://localhost:5173`

---

## Live Demo: Crisis Injection

Vantage Point includes a **live crisis simulation tool** for demo purposes. This injects realistic signals into the database so the AI agents can detect and synthesize them in real-time.

```bash
# Inject a crisis (5 scenarios available)
python -m tools.simulate_crisis --scenario client_loss
python -m tools.simulate_crisis --scenario funding_pull
python -m tools.simulate_crisis --scenario key_hire_quit
python -m tools.simulate_crisis --scenario data_breach
python -m tools.simulate_crisis --scenario competitor

# Then click "Synthesize Intelligence" in the UI to see the AI react

# Clean up injected data
python -m tools.simulate_crisis --reset
```

---

## Docker Deployment

```bash
# Build
docker build -t vantage-point .

# Run
docker run -p 8000:8000 -e GEMINI_API_KEY=your-key vantage-point

# Open http://localhost:8000
```

---

## Cloud Run Deployment

```bash
# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/vantage-point

# Deploy
gcloud run deploy vantage-point \
  --image gcr.io/YOUR_PROJECT/vantage-point \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your-key
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Service liveness check |
| `POST` | `/api/brief` | Trigger full multi-agent intelligence synthesis |
| `POST` | `/api/ask` | Ask a specific natural language question |
| `GET` | `/api/dashboard-data` | Aggregated data for the React dashboard |
| `GET` | `/api/okrs` | Current OKR scores and progress |
| `GET` | `/api/risks` | Active risk flags |
| `GET` | `/api/signals` | Detected communication signals |
| `GET` | `/api/alerts` | Proactive alerts from health monitoring |
| `GET` | `/api/history` | Historical intelligence briefs |
| `POST` | `/api/alerts/{id}/ack` | Acknowledge a proactive alert |

---

## Key Differentiators

1. **Multi-Agent Orchestration** — 4 specialized agents run in parallel, each with a distinct intelligence domain
2. **MCP Integration** — Three FastMCP servers for standardized, secure access to Google Workspace tools
3. **Live AI Synthesis** — Gemini 2.5 Flash generates narrative briefs from structured data in real-time (not pre-baked)
4. **Proactive Alerting** — Automatic health degradation detection triggers alerts without user intervention
5. **Premium UI** — "Lumina Ether" design system with glassmorphism, aurora gradients, and editorial typography
6. **Crisis Simulation** — Built-in tool for live demo injection to prove end-to-end agent detection

---


