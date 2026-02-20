
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
```
