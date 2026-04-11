# Frontend TypeScript Migration Plan

Migrate the Hybrid Hour frontend from JavaScript to strict TypeScript while maintaining the existing React + Vite + Docker Compose setup.

---

## Prerequisites

- Current stack: React 18 + Vite 6 + Tailwind CSS 4
- Target: Full strict TypeScript with zero `any` types
- Keep existing Docker Compose workflow unchanged

---

## Phase 1: Setup & Configuration

### 1. Install TypeScript Dependencies

```bash
cd frontend
npm install --save-dev typescript @types/react @types/react-dom @types/node
npm install --save-dev @typescript-eslint/eslint-plugin @typescript-eslint/parser
```

### 2. Create `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/api/*": ["src/api/*"],
      "@/types/*": ["src/types/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 3. Create `tsconfig.node.json`

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

### 4. Update `vite.config.ts` (rename from .js)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true,
    port: 5173,
  },
});
```

### 5. Update ESLint Config

Add to `eslint.config.js`:
```javascript
import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.strictTypeChecked],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        project: ['./tsconfig.json'],
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/explicit-function-return-type': 'warn',
    },
  }
);
```

---

## Phase 2: Type Definitions

### Create `src/types/index.ts`

Define all domain types first:

```typescript
// Workout Types
export interface WorkoutStep {
  name: string;
  duration_mins: number;
  intensity_factor: number;
}

export interface WorkoutBlock {
  name: string;
  repeat_count: number;
  steps: WorkoutStep[];
}

export interface Workout {
  workout_id: string;
  title: string;
  modality: Modality;
  focus: Focus;
  description: string;
  structure: WorkoutBlock[];
  tss: number;
  is_user_created?: boolean;
}

export type Modality = 'Running' | 'Cycling' | 'Swimming' | 'Strength' | 'Conditioning' | 'Hypertrophy' | 'Rest';

export type Focus = 'Aerobic Low' | 'Aerobic High' | 'VO2 Max' | 'Threshold' | 'Anaerobic' | 'Strength' | 'Hypertrophy' | 'Rest';

// Calendar Types
export interface CalendarDay {
  day_index: number;
  workout_id: string | null;
  title: string | null;
  modality: Modality | null;
  focus: Focus | null;
  description: string | null;
  structure: WorkoutBlock[] | null;
  tss: number;
  is_user_locked: boolean;
  is_user_created?: boolean;
}

// API Types
export interface BuildWorkoutRequest {
  user_inputs: Partial<Workout>;
  natural_language_prompt?: string;
}

export interface BuildWorkoutResponse {
  workout: Workout | null;
  generation_mode: 'manual' | 'rag_match' | 'synthetic';
  match_confidence: number | null;
  errors: string[];
}

export interface PlanSummary {
  id: string;
  plan_name: string;
  user_goal: string;
  created_at: string;
  total_tss: number;
}

// User Types
export interface User {
  id: string;
  username: string;
  email: string;
}

export interface AuthContextType {
  isLoggedIn: boolean;
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
}

// Planner Hook Return Type
export interface UsePlannerReturn {
  days: CalendarDay[];
  cycleLength: number;
  setCycleLength: (length: number) => void;
  loading: boolean;
  suggestPlan: (userGoal: string) => Promise<{ success: boolean; error?: string }>;
  savePlan: (userGoal: string) => Promise<void>;
  toggleLock: (idx: number) => void;
  clearPlan: () => void;
  reasoning: string;
  fetchLatest: () => Promise<void>;
  savedPlans: PlanSummary[];
  currentPlanId: string | null;
  fetchAllPlans: () => Promise<void>;
  loadPlan: (planId: string) => Promise<void>;
  addWorkout: (dayIndex: number, workoutData: Workout) => void;
  editWorkout: (dayIndex: number, workoutData: Partial<Workout>) => void;
  deleteWorkout: (dayIndex: number) => void;
  addRestDay: (dayIndex: number) => void;
  buildWorkout: (userInputs: Partial<Workout>, naturalLanguagePrompt?: string) => Promise<BuildWorkoutResponse>;
}
```

---

## Phase 3: File Migration Order

Migrate in this order (bottom-up, starting with utilities):

### Priority 1: API & Types (Day 1)
1. `src/api/client.js` → `src/api/client.ts`
2. `src/types/index.ts` (new file)

### Priority 2: Hooks (Day 1-2)
3. `src/hooks/useAuth.jsx` → `src/hooks/useAuth.ts`
4. `src/hooks/usePlanner.jsx` → `src/hooks/usePlanner.ts` (complex - 300+ lines)

### Priority 3: UI Components (Day 2-3)
5. `src/components/ui/Button.jsx` → `src/components/ui/Button.tsx`
6. `src/components/ui/DayCard.jsx` → `src/components/ui/DayCard.tsx`
7. `src/components/ui/WorkoutModal.jsx` → `src/components/ui/WorkoutModal.tsx`
8. `src/components/ui/WorkoutEditorModal.jsx` → `src/components/ui/WorkoutEditorModal.tsx`
9. `src/components/ui/PlanSelector.jsx` → `src/components/ui/PlanSelector.tsx`

### Priority 4: Pages (Day 3)
10. `src/pages/Login.jsx` → `src/pages/Login.tsx`
11. `src/pages/Register.jsx` → `src/pages/Register.tsx`
12. `src/pages/Home.jsx` → `src/pages/Home.tsx` (complex - 350+ lines)

### Priority 5: Entry Points (Day 3)
13. `src/main.jsx` → `src/main.tsx`
14. `src/App.jsx` → `src/App.tsx`

---

## Phase 4: Component Migration Examples

### Example: Button Component

**Before (Button.jsx):**
```javascript
export const Button = ({ children, onClick, variant = 'primary', disabled, className = '' }) => {
  // ...
};
```

**After (Button.tsx):**
```typescript
import type { ReactNode, MouseEventHandler } from 'react';

interface ButtonProps {
  children: ReactNode;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  variant?: 'primary' | 'outline' | 'ghost';
  disabled?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  disabled = false, 
  className = '',
  type = 'button'
}) => {
  // ... implementation
};
```

### Example: DayCard Component

**Key types needed:**
```typescript
import type { CalendarDay } from '@/types';

interface DayCardProps {
  day: CalendarDay;
  onToggleLock: (index: number) => void;
  onClick: () => void;
  onEdit: (index: number) => void;
  onRestDay?: (index: number) => void;
}
```

### Example: usePlanner Hook

**Key challenge:** Complex state and async functions
```typescript
import { useState, useEffect, useCallback } from 'react';
import type { CalendarDay, Workout, PlanSummary, UsePlannerReturn } from '@/types';

export const usePlanner = (): UsePlannerReturn => {
  const [days, setDays] = useState<CalendarDay[]>([]);
  const [cycleLength, setCycleLength] = useState<number>(7);
  // ...
};
```

---

## Phase 5: Docker Considerations

Good news: **No Dockerfile changes needed!**

Vite handles both `.js` and `.tsx` files transparently. The existing Docker setup will work as-is:

```dockerfile
# Existing Dockerfile continues to work
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev", "--", "--host"]
```

Just ensure `tsconfig.json` is copied in the build stage.

---

## Phase 6: Validation Checklist

Before marking migration complete:

- [ ] Zero TypeScript errors (`npm run build` succeeds)
- [ ] Zero ESLint errors (`npm run lint` passes)
- [ ] All `.jsx` files renamed to `.tsx`
- [ ] No `any` types in application code (allowed only in test files)
- [ ] All API responses have defined interfaces
- [ ] All component props have defined interfaces
- [ ] Docker build succeeds
- [ ] Hot reload works in dev mode
- [ ] Production build works

---

## Commands Summary

```bash
# Install dependencies
npm install -D typescript @types/react @types/react-dom @types/node

# Run type checking
npx tsc --noEmit

# Run linter
npm run lint

# Dev server (unchanged)
npm run dev

# Build (unchanged)
npm run build
```

---

## Time Estimate

- **Phase 1 (Setup)**: 30 minutes
- **Phase 2 (Types)**: 1 hour
- **Phase 3 (Migration)**: 4-6 hours (depending on strictness)
- **Phase 4 (Validation)**: 1-2 hours

**Total: 1-2 days of focused work**

---

## Risk Mitigation

1. **Keep Git commits small**: Commit after each file migration
2. **Test in Docker after each phase**: `docker-compose up --build`
3. **Have rollback plan**: Branch off before starting migration
4. **Use `satisfies` instead of `as`**: For safer type assertions
5. **Don't over-type third-party libs**: Use `@types/*` packages

