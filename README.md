# Situation Room — AI Chief of Staff for Startup Founders

> **Gen AI APAC Edition Hackathon (Cohort 1) — Hack2Skill**

## Problem Statement
> Build a multi-agent AI system that helps users manage tasks, schedules, and information
> by interacting with multiple tools and data sources.

**Situation Room** is a proactive AI that monitors a founder's Gmail, Google Calendar,
Google Drive, and internal OKR database to surface risks, score goal progress, and
deliver prioritized action briefs — like an automated Chief of Staff.

---

## Architecture

```
                         ┌─────────────────────┐
                         │   React Dashboard    │
                         │  (Situation Room UI) │
                         └──────────┬──────────┘
                                    │ REST
                         ┌──────────▼──────────┐
                         │   FastAPI (main.py)  │
                         │  API Layer + Auth    │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │     Orchestrator Agent         │
                    │  Plans • Delegates • Assembles │
                    └──────┬────┬────┬────┬─────────┘
                           │    │    │    │
              ┌────────────┘    │    │    └────────────┐
              ▼                 ▼    ▼                 ▼
        Signal Watcher    OKR Tracker  Risk Spotter   Advisor
        (Gmail MCP)       (Drive MCP)  (Calendar MCP) (Gemini)
              │                 │           │            │
              └─────────────────┴───────────┘            │
                        │                                │
                 ┌──────▼──────┐                 ┌──────▼──────┐
                 │  MCP Servers │                 │ Google       │
                 │  (FastMCP)   │                 │ Gemini API   │
                 └──────┬──────┘                 └─────────────┘
                        │
                 ┌──────▼──────┐
                 │   SQLite DB  │
                 │ OKRs, Risks  │
                 │ Signals, etc │
                 └─────────────┘
```

---

## Core Requirements Coverage

| Requirement | Implementation |
|---|---|
| Primary agent coordinating sub-agents | `OrchestratorAgent` dispatches 4 sub-agents in parallel |
| Structured database | SQLite via SQLAlchemy — OKRs, signals, risks, briefs, alerts |
| Multiple MCP tools | 3 FastMCP servers: Gmail, Google Calendar, Google Drive |
| Multi-step workflows | Signal → OKR score → Risk detect → Gemini synthesis → Brief |
| API-based deployment | FastAPI with 10+ REST endpoints, deployed on Cloud Run |

---

## Tech Stack

- **LLM**: Google Gemini 2.0 Flash (via `google-genai` SDK)
- **Backend**: FastAPI + Python 3.12
- **Frontend**: React + Vite
- **Database**: SQLite + SQLAlchemy ORM
- **MCP**: FastMCP (Model Context Protocol) servers
- **Deployment**: Docker → Google Cloud Run

---

## Project Structure

```
situation-room/
├── agents/
│   ├── orchestrator.py      # Primary coordinating agent
│   ├── signal_watcher.py    # Gmail sub-agent
│   ├── okr_tracker.py       # OKR scoring sub-agent
│   ├── risk_spotter.py      # Risk detection sub-agent
│   ├── advisor.py           # Gemini-powered synthesis
│   └── scheduler.py         # Proactive alerting
├── db/
│   ├── models.py            # SQLAlchemy ORM models
│   └── database.py          # DB connection + session
├── tools/
│   └── mcp_client.py        # MCP tool wrappers
├── mcp_servers/
│   ├── gmail_server.py      # FastMCP Gmail server
│   ├── calendar_server.py   # FastMCP Calendar server
│   └── drive_server.py      # FastMCP Drive server
├── frontend/                # React dashboard (Vite)
│   ├── src/
│   │   ├── components/      # Dashboard UI components
│   │   ├── App.jsx          # Main app + state management
│   │   ├── api.js           # Backend API client
│   │   └── index.css        # Design system
│   └── ...
├── data/
│   └── seed.py              # Demo data seeder
├── main.py                  # FastAPI entry point
├── Dockerfile               # Multi-stage Docker build
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Create .env with your Gemini API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Seed Demo Data
```bash
python -m data.seed
```

### 3. Run Backend
```bash
uvicorn main:app --reload --port 8000
```

### 4. Run Frontend (development)
```bash
cd frontend
npm run dev
```

### 5. Open Dashboard
Navigate to `http://localhost:5173`

---

## Docker Deployment

```bash
# Build
docker build -t situation-room .

# Run
docker run -p 8000:8000 -e GEMINI_API_KEY=your-key situation-room

# Open http://localhost:8000
```

---

## Cloud Run Deployment

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR_PROJECT/situation-room

# Deploy
gcloud run deploy situation-room \
  --image gcr.io/YOUR_PROJECT/situation-room \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your-key
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Liveness check |
| `POST` | `/api/brief` | Generate full situation brief |
| `POST` | `/api/ask` | Ask a specific question |
| `GET` | `/api/dashboard-data` | All data for dashboard |
| `GET` | `/api/okrs` | Current OKR scores |
| `GET` | `/api/risks` | Active risks |
| `GET` | `/api/signals` | Gmail signals |
| `GET` | `/api/alerts` | Proactive alerts |
| `GET` | `/api/history` | Past briefs |

---

## Differentiators

1. **Proactive alerting** — Automatically detects health degradation and creates alerts
2. **MCP integration** — Three FastMCP servers for standardized tool access
3. **Parallel agent execution** — Sub-agents run concurrently via asyncio
4. **Google Gemini** — AI synthesis powered by Gemini 2.0 Flash
5. **Production dashboard** — React frontend with glassmorphism UI

---

## Team
Built for Gen AI APAC Edition Hackathon — Cohort 1 by Hack2Skill
