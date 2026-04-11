# Hybrid Hour Enhancement Plan

Add user workout creation/editing, improve LLM context awareness, distinct rest day styling, and enhanced TSS metrics across the training calendar.

---

## 1. User-Created Workouts (Add + Edit)

**Goal**: Allow users to manually add custom workouts to any day and edit existing ones.

### Frontend Changes

- **New Component**: `WorkoutEditorModal.jsx` - A form for creating/editing workouts with fields:
  - Title (text input)
  - Modality (dropdown: Running, Cycling, Strength, etc.)
  - Focus (dropdown: Aerobic Low, VO2 Max, etc.)
  - Description (textarea)
  - Structure (optional array of steps)
- **Update `usePlanner.jsx`**:
  - Add `addWorkout(dayIndex, workoutData)` function
  - Add `editWorkout(dayIndex, workoutData)` function
  - Add `deleteWorkout(dayIndex)` function
  - Add `addRestDay(dayIndex)` function - instant rest day with one tap
- **Update `DayCard.jsx`**:
  - Add "+" button on empty days to trigger add modal
  - Add context menu or edit button on existing workouts
  - Visual indicator for user-created vs AI-generated workouts
  - **Empty Day Split Buttons**: 2/3 "Add Workout" + 1/3 "Rest" for fast rest day selection
- **Update `Home.jsx`**:
  - Add state for `editingDay` to handle the editor modal
  - Pass edit handlers down to DayCard

### Backend Changes (Optional - can be frontend-only)

- Workouts are currently stored in the calendar JSON, so no DB changes needed immediately
- Future: Could add `is_user_created` flag to track provenance

---

## 2. Enhanced LLM Context

**Goal**: Give the LLM richer context about the current calendar state when generating suggestions.

### Backend Changes

- **Update `analyzer.py`**:
  - Currently sends: `modality | focus | Locked: true/false`
  - Enhance to include: `title | TSS | is_user_created` flag
  - Example new format:
    ```xml
    <day index='0' locked='true' user_created='true' tss='85'>Running | Aerobic High | Morning 10k Tempo</day>
    ```
- **Update `SYSTEM_PROMPT`** in `prompts.py`:
  - Instruct LLM to respect user-created workouts as higher priority than locked workouts
  - Tell LLM to consider TSS balance when suggesting around user workouts

---

## 3. Distinct Rest Day Styling

**Goal**: Make rest days visually distinct from empty/unassigned days.

### Frontend Changes

- **Update `DayCard.jsx`**:
  - Detect rest days: `day.modality === "Rest"` OR (`!day.workout_id && day.tss === 0` as rest indicator)
  - Apply muted styling: gray/blue tint instead of neon highlight
  - Show "REST DAY" text instead of empty state
  - Use `BatteryCharging` icon (Lucide React) for rest days - conveys "recharging/recovery"
- **Update `WorkoutModal.jsx`**:
  - Different header styling for rest days
  - Show rest-specific messaging ("Recovery is training")

---

## 4. TSS Metrics Dashboard

**Goal**: Show weekly and total TSS metrics to help users track training load.

### Frontend Changes

- **Update `Home.jsx`**:
  - Add TSS summary section above the calendar
  - Show: Weekly TSS totals, Average daily TSS, Total block TSS
  - Visual indicator for TSS distribution (low/medium/high load days)
- **Update `DayCard.jsx`**:
  - Already shows TSS - enhance with color coding:
    - Low (< 50): Green tint
    - Medium (50-100): Yellow tint
    - High (> 100): Red tint
- **New Component**: `TSSChart.jsx` (optional future enhancement)
  - Bar chart showing TSS across the 14 days

---

## Additional Suggestions

Based on the current architecture, here are bonus features that would enhance the experience:

1. **Workout Templates**: Let users save their custom workouts as templates for quick reuse
2. **Drag & Drop Reordering**: Allow users to drag workouts between days to reshuffle their plan
3. **TSS Target Setting**: Let users set a weekly TSS target and show progress bar
4. **Weekly Recovery Recommendation**: LLM suggests which days should be rest based on load distribution
5. **Workout Swap**: One-click "swap this workout for similar" button using the retriever node

---

## 5. Custom Workout Builder Graph (New Feature)

**Goal**: A dedicated LLM graph for creating/editing single-day workouts that handles both structured user input AND AI-assisted generation with RAG matching.

### User Flows Supported

1. **Expert Mode**: User inputs exact workout structure (title, modality, focus, duration, steps, intensity) - LLM validates and formats
2. **Assisted Mode**: User types "I want a 45min tempo run" - LLM uses RAG to find matching workouts or generates one
3. **Hybrid Mode**: User fills some fields + adds natural language prompt - LLM combines both

### Backend Changes

- **New State**: `WorkoutBuilderState` with fields:
  - `user_inputs`: Partial workout data from form
  - `natural_language_prompt`: Optional AI request text
  - `matched_workout`: Best RAG match from DB (if any)
  - `final_workout`: Fully structured workout object
  - `generation_mode`: "manual", "rag_match", or "synthetic"
- **New Graph**: `workout_builder_graph.py`
  - Node 1: `intake_node` - Parse user inputs + natural language
  - Node 2: `matcher_node` - Run RAG search if natural language present
  - Node 3: `builder_node` - Either format manual input OR adapt matched workout OR generate synthetic
  - Node 4: `validator_node` - Validate structure, calculate TSS, ensure 60min constraint
- **New Endpoint**: `POST /workouts/build` - Takes partial inputs + optional prompt, returns complete workout
- **Reuse existing**: `search_workouts_filtered()` for RAG, `generate_synthetic_workout()` adapted for single-day

### Frontend Changes

- **Update `WorkoutEditorModal.jsx`**:
  - Add toggle: "Manual Entry" vs "AI Assist"
  - Manual: Show all form fields (title, modality, focus, structure)
  - AI Assist: Show natural language input + preview of matched/generated workout
  - Display RAG match confidence if applicable
  - Allow user to accept match, regenerate, or switch to manual

## 6. Plan Listing & Loading (New Feature)

**Goal**: Allow users to view all their saved plans and load a specific one.

### Current State

- Backend has `GET /calendar/latest` endpoint (returns most recent plan only)
- Frontend has `fetchLatest()` in `usePlanner` that only loads the latest plan

### Backend Changes

- **New endpoint**: `GET /calendar/plans` - Returns list of user's saved plans (id, plan_name, created_at)
- **New endpoint**: `GET /calendar/plans/{plan_id}` - Returns specific plan by ID
- **Update models** (if needed): Ensure plan_name is searchable/sortable

### Frontend Changes

- **New Component**: `PlanSelector.jsx` - Dropdown or modal showing all saved plans
  - Display: Plan name, creation date, TSS summary
  - Actions: Load, Delete (optional)
- **Update `usePlanner.jsx`**:
  - Add `fetchAllPlans()` to get list
  - Add `loadPlan(planId)` to load specific plan
  - Add `savedPlans[]` state
- **Update `Home.jsx`**:
  - Add "My Plans" button/dropdown in header
  - Show current plan name when loaded

---

## Implementation Priority

**Phase 1 (Core)**: User workout add/edit with AI Builder + Rest day styling + Plan listing
**Phase 2 (Smart AI)**: Enhanced LLM context (main planning graph)
**Phase 3 (Metrics)**: TSS dashboard + visual enhancements

---

## Files to Modify

| File                                                | Changes                                                         |
| --------------------------------------------------- | --------------------------------------------------------------- |
| `frontend/src/hooks/usePlanner.jsx`                 | Add CRUD functions for workouts, plan loading, addRestDay       |
| `frontend/src/components/ui/DayCard.jsx`            | Add edit/add buttons, rest day styling, split empty-day buttons |
| `frontend/src/components/ui/WorkoutModal.jsx`       | Rest day styling                                                |
| `frontend/src/components/ui/WorkoutEditorModal.jsx` | **NEW** - Create/edit form with AI Assist toggle                |
| `frontend/src/components/ui/PlanSelector.jsx`       | **NEW** - Plan list dropdown/modal                              |
| `frontend/src/pages/Home.jsx`                       | Add TSS summary, editor modal, plan selector                    |
| `backend/api/endpoints/calendar.py`                 | Add plan list & fetch endpoints                                 |
| `backend/api/endpoints/workouts.py`                 | Add `POST /workouts/build` endpoint                             |
| `backend/agents/nodes/workout_builder/`             | **NEW** - Graph, nodes, state, prompts                          |
| `backend/agents/nodes/analyzer.py`                  | Enhance calendar XML format                                     |
| `backend/agents/prompts.py`                         | Update system prompt instructions                               |

