# ⚡ Hybrid Hour | AI-Powered Training Orchestrator

An intelligent, stateful training platform that transforms natural language fitness "missions" into elite 14-day hybrid training plans. Powered by **Llama 3.3**, **LangGraph**, and **Vector Search**.

## 🚀 Live Demo
**[View Live App](https://hybrid-hour.ddnsfree.com)** (Deployed on GCP with Nginx/SSL)

---

## 🧠 The Intelligence Engine
Unlike standard LLM wrappers, Hybrid Hour uses a **Stateful Multi-Node Graph** to ensure athletic integrity:

1.  **Analyzer Node**: Deconstructs user goals (e.g., "Prep for HYROX but keep my 5k speed") into specific modality constraints.
2.  **Retriever Node (RAG)**: Performs a semantic search using **pgvector** and **Hugging Face (all-MiniLM-L6-v2)** to match goals against a curated library of 60+ elite workouts.
3.  **Summarizer Node**: Condenses complex AI reasoning into a concise "Coach's Briefing" for the athlete.

## 🛠️ Technical Stack
- **Backend**: FastAPI (Async), SQLAlchemy 2.0, Gunicorn/Uvicorn.
- **Frontend**: React (Vite 6), Tailwind CSS 4 (Oxide Engine), Node.js 22.
- **AI/LLM**: LangGraph, Groq (Llama 3.3), Sentence-Transformers.
- **Database**: Neon Postgres (Serverless) with `pgvector` extension.
- **DevOps**: Google Compute Engine (GCE), Linux Systemd, Nginx, Certbot SSL.

## 📈 Key Features
- **Semantic Workout Retrieval**: Matches "Vibe" and "Focus" of training to technical sessions via 384-dimension vector embeddings.
- **Complex TSS Logic**: Custom mathematical modelling to calculate **Training Stress Score (TSS)** and Intensity Factors (IF) for every generated session.
- **Production-Grade Infrastructure**: Full background process management and encrypted TLS traffic.

## 🛠️ Local Development

1. **Clone & Install Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

## File Structure
```
backend/
├── main.py                 # App entry point, middleware, & router inclusion
├── deps.py                 # FastAPI dependencies (get_db, get_current_user)
├── auth.py                 # JWT token logic & authentication flow
├── seed.py                 # Script to populate DB with initial 50 workouts
├── .env                    # Secrets (DATABASE_URL, SECRET_KEY, HF_TOKEN)
├── alembic.ini             # Database migration configuration
│
├── agents/                 # THE BRAIN: LangGraph & LLM Logic
│   ├── graph.py            # StateGraph definition & edge logic
│   ├── state.py            # TypedDict for the 14-day calendar state
│   ├── prompts.py          # System messages & sports science rules
│   └── nodes/              # Individual "Thinking" steps
│       ├── analyzer.py     # Checks for user-locked workouts
│       ├── retriever.py    # Logic to query pgvector (The RAG step)
│       └── validator.py    # Prevents overtraining/interference effects
│
├── api/                    # THE PLUMBING: Web Layer
│   ├── endpoints/          # Route handlers
│   │   ├── workouts.py     # CRUD for workout library
│   │   ├── calendar.py     # CRUD for user's 14-day plan
│   │   └── user.py         # Profile & FTP settings
│   └── services/           # Business Logic Tools
│       ├── embeddings.py   # HuggingFace local embedding logic
│       └── tss_calc.py     # The IF² based TSS math we built
│
├── core/                   # THE RULES: Global Config
│   ├── config.py           # Pydantic Settings (env var management)
│   └── security.py         # Password hashing & encryption helpers
│
├── database/               # THE DATA: Connection Management
│   ├── session.py          # Async engine & sessionmaker setup
│   └── base.py             # Global Base for Alembic (imports all models)
│
├── models/                 # THE STORAGE: SQLAlchemy Tables (DB)
│   ├── workout.py          # Workout table with pgvector(384)
│   ├── plan.py             # User's calendar state table
│   └── user.py             # User auth & metrics table
│
├── schemas/                # THE CONTRACT: Pydantic Models (API)
│   ├── workout.py          # HybridWorkoutSchema, Block, Step
│   ├── plan.py             # Calendar schemas
│   └── user.py             # Auth & Token schemas
│
└── migrations/             # THE HISTORY: Alembic Versions
    └── versions/           # Individual .py migration files

frontend/src/
├── api/                # Axios client
├── components/         # Shared UI (Button, Input, Navbar)
├── features/           # Logic-heavy features
│   ├── auth/           # Login/Register forms & logic
│   └── planner/        # Calendar & AI Suggest logic
├── pages/              # The actual "Screens"
│   ├── Home.jsx        # Your Workout Planner
│   ├── Login.jsx       # Login Screen
│   └── Register.jsx    # Register Screen
├── assets/             # CSS files
├── App.jsx             # Router Configuration
└── main.jsx            # Entry point


```
