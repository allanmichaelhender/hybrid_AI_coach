# ⚡ Hybrid Hour | AI-Powered Training Orchestrator

An intelligent, stateful training platform that transforms natural language fitness "missions" into elite training plans. Powered by **Llama 3.3**, **LangGraph**, and **Vector Search**.

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
- **Database**: PostgreSQL 16 with `pgvector` extension (Dockerized).
- **DevOps**: Docker Compose, Google Compute Engine (GCE), Nginx, Certbot SSL.

## � API Endpoints

All API endpoints use the `/api/v1/` prefix:

- `POST /api/v1/calendar/suggest` - Generate AI training plan
- `POST /api/v1/calendar/save` - Save training plan
- `GET /api/v1/calendar/plans` - Get user's saved plans
- `GET /api/v1/calendar/latest` - Get latest saved plan
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

## �📈 Key Features

- **Semantic Workout Retrieval**: Matches "Vibe" and "Focus" of training to technical sessions via 384-dimension vector embeddings.
- **Complex TSS Logic**: Custom mathematical modelling to calculate **Training Stress Score (TSS)** and Intensity Factors (IF) for every generated session.
- **Rich Workout Cards**: Display focus, structure preview, main movements, difficulty rating, and modality icons.
- **User Control**: Lock workouts to prevent AI modifications, delete workouts directly from cards, manual workout editing.
- **Guest Mode**: Generate plans without authentication, save plans when logged in.
- **Responsive Layout**: Split-screen design with calendar on left, AI prompt and coach logic on right.
- **Production-Grade Infrastructure**: Docker Compose orchestration, SSL encryption, automatic certificate renewal.

## 🛠️ Local Development

### Docker Setup (Recommended)

1. **Clone & Environment Setup**

   ```bash
   git clone <repo-url>
   cd hybrid_AI_coach
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Start All Services**

   ```bash
   docker compose up -d
   ```

3. **Run Database Migrations**

   ```bash
   docker compose exec backend sh -c "cd /app/backend && alembic upgrade head"
   ```

4. **Seed Database with Workouts**
   ```bash
   docker compose exec backend sh -c "cd /app/backend && python scripts/seed_all.py"
   ```

### Manual Setup (Development)

1. **Clone & Install Backend**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Install Frontend**
   ```bash
   cd frontend
   npm install
   ```

## 🔧 Environment Variables

Required environment variables in `.env`:

- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgresql+asyncpg://user:password@db:5432/hybrid_coach`)
- `API_V1_STR` - API version prefix (default: `/api/v1`)
- `SECRET_KEY` - JWT secret key for authentication
- `GROQ_API_KEY` - Groq API key for Llama 3.3 access
- `PROJECT_NAME` - Project name (default: "Hybrid Hour")

## 🔒 SSL Certificate Setup

### Initial Setup

1. **Create certbot directories on host**

   ```bash
   sudo mkdir -p /etc/letsencrypt
   sudo mkdir -p /var/www/certbot
   ```

2. **Obtain SSL certificate**

   ```bash
   docker run -it --rm \
     -v /etc/letsencrypt:/etc/letsencrypt \
     -v /var/www/certbot:/var/www/certbot \
     certbot/certbot certonly --webroot \
     -w /var/www/certbot \
     -d your-domain.com
   ```

3. **Enable HTTPS in nginx** (uncomment HTTPS server block in `nginx/default.conf`)

### Automatic Renewal

1. **Create renewal script**

   ```bash
   sudo nano /usr/local/bin/renew-ssl.sh
   ```

   ```bash
   #!/bin/bash
   docker run --rm -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot:/var/www/certbot certbot/certbot renew --quiet && docker compose restart nginx
   ```

2. **Make executable**

   ```bash
   sudo chmod +x /usr/local/bin/renew-ssl.sh
   ```

3. **Add to crontab**
   ```bash
   sudo crontab -e
   ```
   ```
   0 3 * * * /usr/local/bin/renew-ssl.sh
   ```

## 🚀 Deployment

### GCP Deployment Checklist

1. **Create GCP Compute Engine instance**
2. **Install Docker and Docker Compose**
3. **Clone repository**
4. **Configure firewall rules** (ports 80, 443, 5173, 8000)
5. **Set up `.env` file** with production values
6. **Run docker compose up -d**
7. **Run database migrations**
8. **Seed database**
9. **Configure SSL certificates**
10. **Set up automatic SSL renewal**

### Docker Commands Reference

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f [service-name]

# Rebuild specific service
docker compose up -d --build [service-name]

# Execute command in container
docker compose exec [service-name] [command]

# View running services
docker compose ps

# Clean up unused images and containers
docker system prune -a
```

## 📁 File Structure

```
backend/
├── main.py                 # App entry point, middleware, & router inclusion
├── deps.py                 # FastAPI dependencies (get_db, get_current_user)
├── auth.py                 # JWT token logic & authentication flow
├── scripts/
│   └── seed_all.py          # Script to populate DB with workout library
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
├── alembic/                # Database migrations
│   ├── versions/           # Migration files
│   └── env.py              # Migration environment
├── data/                   # Workout data libraries
│   ├── swim_library.py
│   ├── cycling_library.py
│   ├── running_library.py
│   └── ...
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

frontend/src/
├── api/                # Axios client
├── components/         # Shared UI components
│   └── ui/             # Button, DayCard, WorkoutModal, WorkoutEditorModal, PlanSelector
├── features/           # Logic-heavy features
│   └── auth/           # Login/Register forms & logic
├── hooks/              # Custom React hooks
│   ├── useAuth.tsx     # Authentication state management
│   └── usePlanner.tsx  # Calendar & AI Suggest logic
├── pages/              # The actual "Screens"
│   ├── Home.tsx        # Your Workout Planner
│   ├── Login.tsx       # Login Screen
│   └── Register.tsx    # Register Screen
├── types/              # TypeScript type definitions
├── App.tsx             # Router Configuration
└── main.tsx            # Entry point


```
