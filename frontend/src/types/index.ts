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

export type Modality =
  | "Running"
  | "Cycling"
  | "Swimming"
  | "Strength"
  | "Conditioning"
  | "Hypertrophy"
  | "Rest";

export type Focus =
  | "Aerobic Low"
  | "Aerobic High"
  | "VO2 Max"
  | "Threshold"
  | "Anaerobic"
  | "Strength"
  | "Hypertrophy"
  | "Rest";

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
  success: boolean;
  workout?: Workout | null;
  generation_mode?: "manual" | "rag_match" | "synthetic";
  match_confidence?: number | null;
  errors?: string[];
  error?: string;
}

export interface PlanSummary {
  id: string;
  plan_name: string;
  user_goal: string;
  created_at: string;
  total_tss: number;
}

export interface SavePlanRequest {
  plan_name: string;
  user_goal: string;
  calendar_data: CalendarDay[];
  coach_reasoning?: string;
}

export interface CalendarRequest {
  calendar: CalendarDay[];
  cycle_length: number;
  user_goal: string;
}

export interface CalendarUpdateResponse {
  updated_calendar: CalendarDay[];
  coach_reasoning: string;
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
  suggestPlan: (
    userGoal: string,
  ) => Promise<{ success: boolean; error?: string }>;
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
  buildWorkout: (
    userInputs: Partial<Workout>,
    naturalLanguagePrompt?: string,
  ) => Promise<BuildWorkoutResponse>;
}

// Component Props Types
export interface ButtonProps {
  children: React.ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  variant?: "primary" | "outline" | "ghost";
  disabled?: boolean;
  className?: string;
  type?: "button" | "submit" | "reset";
}

export interface DayCardProps {
  day: CalendarDay;
  onToggleLock: (index: number) => void;
  onClick: () => void;
  onEdit: (index: number) => void;
  onRestDay?: (index: number) => void;
}

export interface WorkoutModalProps {
  day: CalendarDay | null;
  isOpen: boolean;
  onClose: () => void;
}

export interface WorkoutEditorModalProps {
  isOpen: boolean;
  onClose: () => void;
  dayIndex: number | null;
  day: CalendarDay | null;
  onSave: (dayIndex: number, data: Workout) => void;
  onDelete: (dayIndex: number) => void;
  buildWorkout: (
    userInputs: Partial<Workout>,
    naturalLanguagePrompt?: string,
  ) => Promise<BuildWorkoutResponse>;
}

export interface PlanSelectorProps {
  isOpen: boolean;
  onClose: () => void;
  plans: PlanSummary[];
  currentPlanId: string | null;
  onLoadPlan: (planId: string) => Promise<void>;
  onFetchPlans: () => Promise<void>;
  loading: boolean;
}
