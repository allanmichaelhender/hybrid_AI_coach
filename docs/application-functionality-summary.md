# Hybrid Hour - Application Functionality Summary

## Overview

Hybrid Hour is an AI-powered training orchestrator that transforms natural language fitness goals into elite training plans. The application uses a stateful multi-node AI graph powered by Llama 3.3, LangGraph, and vector search to generate personalized workout schedules.

## Architecture

### Frontend (React + Vite + Tailwind CSS)

**Tech Stack:**
- React with TypeScript
- Vite 6 for build tooling
- Tailwind CSS 4 (Oxide Engine) for styling
- React Router for navigation
- Axios for API communication

**Key Pages:**
- `Home.tsx` - Main training planner interface with calendar and AI prompt
- `Login.tsx` - User authentication
- `Register.tsx` - User registration

**Custom Hooks:**
- `useAuth.tsx` - Manages authentication state (login/logout, JWT token handling)
- `usePlanner.tsx` - Core planner logic managing calendar state, AI suggestions, plan CRUD operations

**UI Components:**
- `DayCard.tsx` - Individual workout day card with lock/edit/delete functionality
- `WorkoutModal.tsx` - Displays workout details when clicking a day card
- `WorkoutEditorModal.tsx` - Manual workout editing/creation interface
- `PlanSelector.tsx` - Dropdown to select/load saved plans
- `Button.tsx` - Reusable button component

**Frontend Features:**
- Split-screen layout: calendar grid (left) + AI prompt + coach reasoning (right)
- 7-day or 14-day cycle toggle
- TSS (Training Stress Score) metrics display (total, average, weekly breakdown)
- Lock workouts to prevent AI modifications
- Manual workout editing/creation/deletion
- Guest mode (localStorage persistence) vs authenticated mode (cloud sync)
- Plan saving/loading from database

### Backend (FastAPI + SQLAlchemy + PostgreSQL)

**Tech Stack:**
- FastAPI with async support
- SQLAlchemy 2.0 with async sessions
- PostgreSQL 16 with pgvector extension
- Alembic for database migrations
- Gunicorn/Uvicorn for production

**Key Modules:**

#### `main.py`
- FastAPI application entry point
- CORS middleware configuration
- Router inclusion (auth, calendar, workouts)
- Root endpoint and user profile endpoint

#### `auth.py`
- JWT token generation and validation
- User registration and login endpoints
- Password hashing with bcrypt

#### `deps.py`
- Dependency injection for database sessions
- Current user extraction from JWT tokens

#### `api/api.py`
- Main API router aggregating calendar and workout endpoints

#### `api/endpoints/calendar.py`
- `POST /suggest` - AI-powered training plan generation
- `POST /save` - Save training plan to database
- `GET /plans` - List all saved plans for current user
- `GET /plans/{plan_id}` - Retrieve specific plan by ID
- `GET /latest` - Get most recent saved plan

#### `api/endpoints/workouts.py`
- `POST /build` - Build workouts via manual input, RAG match, or synthetic generation

#### `api/services/embeddings.py`
- Hugging Face sentence-transformers for vector embeddings
- Semantic search using pgvector similarity
- Workout filtering by modality and focus

#### `api/services/tss_calc.py`
- Training Stress Score calculation based on intensity factors
- Custom mathematical modeling for workout stress quantification

### AI Agent System (LangGraph + Llama 3.3)

**Architecture:** Stateful multi-node graph with three sequential processing nodes

#### State Management (`agents/state.py`)
- `AgentState` - TypedDict containing:
  - `calendar` - List of CalendarDay objects
  - `cycle_length` - Number of days in training block (7 or 14)
  - `user_goal` - Natural language fitness goal
  - `ai_reasoning` - List of reasoning strings
  - `errors` - Safety violations
  - `planned_workouts` - Structured workout plan from LLM

#### Node 1: Analyzer (`agents/nodes/analyzer.py`)
**Purpose:** Deconstruct user goals into specific modality constraints

**Process:**
1. Converts current calendar state to XML format
2. Uses Llama 3.3 via Groq API with structured output
3. Applies sports science rules from `SYSTEM_PROMPT`
4. Returns `PlanAnalysis` with:
   - `planned_workouts` - List of `PlannedWorkout` objects (day_index, modality, focus, vector_query)
   - `ai_reasoning` - Technical explanation of plan logic

**LLM Configuration:**
- Model: `llama-3.3-70b-versatile`
- Temperature: 0.1 (deterministic output)
- Structured output enforces schema compliance

#### Node 2: Retriever (`agents/nodes/retriever.py`)
**Purpose:** Match planned workouts against curated workout library using semantic search

**Process:**
1. Iterates through planned workouts from analyzer
2. Skips user-locked days
3. Performs semantic search using pgvector embeddings
4. Filters by modality (Running, Cycling, Swimming, Strength, etc.)
5. Filters by focus (Aerobic Low, Aerobic High, VO2 Max, Anaerobic, etc.)
6. If match found: populates calendar with workout details (title, structure, TSS, description)
7. If no match: generates synthetic workout via `generate_synthetic_workout()`

**Fallback:** Synthetic workout generation creates custom workouts when database lacks matches

#### Node 3: Summarizer (`agents/nodes/summarizer.py`)
**Purpose:** Transform technical reasoning into engaging coach's briefing

**Process:**
1. Takes raw `ai_reasoning` from analyzer
2. Uses Llama 3.3 to restructure into conversational format
3. Focuses on "Why" behind the plan
4. Returns polished reasoning for UI display

#### Graph Flow (`agents/nodes/graph.py`)
```
Entry → Analyzer → Retriever → Summarizer → END
```

### Database Models

#### `User` (models/user.py)
- `id` - UUID primary key
- `username` - Unique identifier
- `hashed_password` - Bcrypt hash
- `plans` - Relationship to UserPlan (cascade delete)

#### `UserPlan` (models/plan.py)
- `id` - UUID primary key
- `user_id` - Foreign key to User
- `plan_name` - Optional plan title
- `user_goal` - Original natural language goal
- `calendar_data` - JSONB array of CalendarDay objects
- `coach_reasoning` - AI-generated explanation
- `created_at` - Timestamp
- `user` - Relationship back to User

#### `Workout` (models/workout.py)
- `id` - UUID primary key
- `title` - Workout name
- `modality` - Training type (Running, Cycling, Swimming, Strength, etc.)
- `focus` - Training intensity (Aerobic Low, Aerobic High, VO2 Max, etc.)
- `calculated_tss` - Pre-computed Training Stress Score
- `description` - Workout description
- `structure` - JSONB array of blocks and steps
- `embedding` - pgvector(384) for semantic search

### Schemas (Pydantic Models)

#### `workout.py`
- `HybridWorkoutSchema` - Full workout structure
- `Block` - Workout block with repeat count
- `Step` - Individual workout step with duration and intensity

#### `calendar.py`
- `CalendarRequest` - Request for AI plan generation
- `CalendarUpdateResponse` - Response with updated calendar and reasoning
- `SavePlanRequest` - Request to save plan
- `SavePlanResponse` - Saved plan data
- `PlanSummary` - Brief plan overview for listing

#### `user.py`
- `UserCreate` - Registration data
- `UserOut` - User profile data
- `Token` - JWT response

## Data Flow

### 1. User Generates Training Plan

```
User enters goal in Home.tsx
    ↓
suggestPlan() calls POST /calendar/suggest
    ↓
Backend invokes LangGraph agent
    ↓
Analyzer Node: Llama 3.3 analyzes goal → planned_workouts + ai_reasoning
    ↓
Retriever Node: Semantic search pgvector → matches workouts to plan
    ↓
Summarizer Node: Llama 3.3 polishes reasoning → coach_reasoning
    ↓
Response returns updated_calendar + coach_reasoning
    ↓
Frontend updates calendar state and displays reasoning
```

### 2. User Saves Plan

```
User clicks SAVE (authenticated)
    ↓
savePlan() calls POST /calendar/save
    ↓
Backend creates UserPlan record with calendar_data JSONB
    ↓
Plan saved to PostgreSQL with user association
    ↓
Frontend shows success message
```

### 3. User Loads Saved Plan

```
User opens PlanSelector dropdown
    ↓
fetchAllPlans() calls GET /calendar/plans
    ↓
Backend returns list of PlanSummary for user
    ↓
User selects plan → loadPlan(planId)
    ↓
GET /calendar/plans/{plan_id}
    ↓
Backend returns full plan with calendar_data
    ↓
Frontend updates calendar state and displays
```

### 4. Manual Workout Editing

```
User clicks edit on DayCard
    ↓
WorkoutEditorModal opens with current workout data
    ↓
User modifies fields or uses AI builder
    ↓
buildWorkout() calls POST /workouts/build
    ↓
Backend runs workout_builder graph (manual/RAG/synthetic modes)
    ↓
Returns generated workout
    ↓
User saves → editWorkout() updates calendar state
```

## Key Features

### AI-Powered Planning
- Natural language goal processing
- Multi-node LangGraph for complex reasoning
- Semantic workout matching via pgvector
- Synthetic workout generation for edge cases
- Coach's reasoning display for transparency

### User Control
- Lock workouts to prevent AI overwrites
- Manual workout creation/editing
- Rest day assignment
- Workout deletion
- Plan reset functionality

### Data Persistence
- Guest mode: localStorage persistence
- Authenticated mode: PostgreSQL cloud sync
- Multiple saved plans per user
- Plan history with timestamps

### Performance Metrics
- TSS (Training Stress Score) calculation
- Intensity Factor (IF) modeling
- Weekly TSS breakdown
- Average daily TSS display

### Workout Library
- 60+ curated elite workouts
- Vector embeddings for semantic search
- Multi-modal support (Running, Cycling, Swimming, Strength, etc.)
- Focus-based filtering (Aerobic, VO2 Max, Anaerobic, etc.)

## API Endpoints Summary

### Authentication (`/api/v1/auth`)
- `POST /register` - User registration
- `POST /login` - User login (returns JWT)
- `GET /me` - Get current user profile

### Calendar (`/api/v1/calendar`)
- `POST /suggest` - Generate AI training plan
- `POST /save` - Save plan to database
- `GET /plans` - List all user plans
- `GET /plans/{plan_id}` - Get specific plan
- `GET /latest` - Get most recent plan

### Workouts (`/api/v1/workouts`)
- `POST /build` - Build workout (manual/RAG/synthetic)

## Deployment

**Infrastructure:**
- Docker Compose orchestration
- Nginx reverse proxy with SSL
- Google Compute Engine (GCE)
- Certbot for automatic SSL renewal

**Services:**
- Frontend (React/Vite)
- Backend (FastAPI)
- PostgreSQL with pgvector
- Nginx (reverse proxy)

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `GROQ_API_KEY` - Llama 3.3 API access
- `API_V1_STR` - API version prefix
- `PROJECT_NAME` - Application name

## Development Workflow

1. **Database Setup:** Run migrations and seed workout library
2. **Backend Development:** FastAPI auto-reloads on changes
3. **Frontend Development:** Vite dev server with HMR
4. **AI Testing:** Test LangGraph nodes independently
5. **Integration:** Full flow from user goal to saved plan

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration for allowed origins
- User-specific plan isolation
- Cascade delete for user data cleanup
