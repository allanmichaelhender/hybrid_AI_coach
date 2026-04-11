import { useState, useEffect, useCallback } from "react";
import api from "../api/client";
import { useAuth } from "./useAuth";
import type {
  CalendarDay,
  Workout,
  PlanSummary,
  UsePlannerReturn,
  BuildWorkoutResponse,
} from "@/types";

function usePlanner(): UsePlannerReturn {
  const { isLoggedIn } = useAuth();
  const [days, setDays] = useState<CalendarDay[]>([]);
  const [cycleLength, setCycleLength] = useState<number>(7);
  const [loading, setLoading] = useState<boolean>(false);
  const [reasoning, setReasoning] = useState<string>("");
  const [savedPlans, setSavedPlans] = useState<PlanSummary[]>([]);
  const [currentPlanId, setCurrentPlanId] = useState<string | null>(null);

  const fetchLatest = useCallback(async (): Promise<void> => {
    if (!isLoggedIn) return;

    setLoading(true);
    try {
      const { data } = await api.get("/calendar/latest");

      if (data && data.calendar_data) {
        setDays(data.calendar_data);
        setReasoning(data.coach_reasoning || "");
        console.log("Cloud Plan Loaded: ", data.plan_name);
      }
    } catch (err) {
      console.error("Failed to load latest plan:", err);
    } finally {
      setLoading(false);
    }
  }, [isLoggedIn]);

  useEffect(() => {
    if (isLoggedIn) {
      fetchLatest();
    }
  }, [isLoggedIn, fetchLatest]);

  // INITIALIZATION: Load data based on Auth Status
  useEffect(() => {
    const savedGuestPlan = localStorage.getItem("guest_plan");

    if (!isLoggedIn && savedGuestPlan) {
      setDays(JSON.parse(savedGuestPlan));
    } else {
      // Default empty 14-day template
      setDays(
        Array.from({ length: 14 }, (_, i) => ({
          day_index: i,
          workout_id: null,
          title: null,
          modality: null,
          focus: null,
          description: null,
          structure: null,
          tss: 0,
          is_user_locked: false,
        })),
      );
    }
  }, [isLoggedIn]);

  // GUEST PERSISTENCE
  useEffect(() => {
    if (!isLoggedIn && days.length > 0) {
      localStorage.setItem("guest_plan", JSON.stringify(days));
    }
  }, [days, isLoggedIn]);

  // THE AI ORCHESTRATOR
  const suggestPlan = async (
    userGoal: string,
  ): Promise<{ success: boolean; error?: string }> => {
    setLoading(true);
    try {
      const response = await api.post("/calendar/suggest", {
        calendar: days.slice(0, cycleLength),
        user_goal: userGoal,
        cycle_length: cycleLength,
        request_scope: "bulk",
      });

      // Update the Calendar State (Deep Merge)
      const newCalendar = days.map((existingDay) => {
        const aiUpdatedDay = response.data.updated_calendar.find(
          (d: CalendarDay) => d.day_index === existingDay.day_index,
        );
        return aiUpdatedDay ? { ...existingDay, ...aiUpdatedDay } : existingDay;
      });
      setDays(newCalendar);

      // Capture & Format Reasoning
      if (response.data.coach_reasoning) {
        setReasoning(response.data.coach_reasoning);
      }

      return { success: true };
    } catch (err: unknown) {
      console.error("AI Planner Error:", err);
      const errorMessage = err instanceof Error ? err.message : "Unknown error";
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const toggleLock = (idx: number): void => {
    setDays((prev) =>
      prev.map((day, i) =>
        i === idx ? { ...day, is_user_locked: !day.is_user_locked } : day,
      ),
    );
  };

  const clearPlan = (): void => {
    if (window.confirm("Are you sure you want to clear your current plan?")) {
      setDays(
        Array.from({ length: 14 }, (_, i) => ({
          day_index: i,
          workout_id: null,
          title: null,
          modality: null,
          focus: null,
          description: null,
          structure: null,
          tss: 0,
          is_user_locked: false,
        })),
      );
      setReasoning("");
    }
  };

  const savePlan = async (userGoal: string): Promise<void> => {
    if (!isLoggedIn) {
      alert("Sign in to save your plan to the cloud! 🚀");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        plan_name: `Mission: ${userGoal}`,
        user_goal: userGoal,
        calendar_data: days,
        coach_reasoning: reasoning,
      };

      const response = await api.post("/calendar/save", payload);

      if (response.status === 201) {
        alert("Plan synced to Neon Cloud! ✅");
      }
    } catch (err) {
      console.error("Save failed:", err);
      alert("Cloud sync failed. Check your connection.");
    } finally {
      setLoading(false);
    }
  };

  // PLAN LOADING FUNCTIONS
  const fetchAllPlans = useCallback(async (): Promise<void> => {
    if (!isLoggedIn) return;

    try {
      const { data } = await api.get("/calendar/plans");
      setSavedPlans(data || []);
    } catch (err) {
      console.error("Failed to fetch plans:", err);
    }
  }, [isLoggedIn]);

  const loadPlan = useCallback(
    async (planId: string): Promise<void> => {
      if (!isLoggedIn) return;

      setLoading(true);
      try {
        const { data } = await api.get(`/calendar/plans/${planId}`);

        if (data && data.calendar_data) {
          setDays(data.calendar_data);
          setReasoning(data.coach_reasoning || "");
          setCurrentPlanId(planId);
          console.log("Loaded plan:", data.plan_name);
        }
      } catch (err) {
        console.error("Failed to load plan:", err);
        alert("Failed to load plan. Please try again.");
      } finally {
        setLoading(false);
      }
    },
    [isLoggedIn],
  );

  // WORKOUT CRUD FUNCTIONS
  const addWorkout = useCallback(
    (dayIndex: number, workoutData: Workout): void => {
      setDays((prev) =>
        prev.map((day, i) =>
          i === dayIndex
            ? {
                ...day,
                workout_id: workoutData.workout_id || `user_${Date.now()}`,
                title: workoutData.title,
                modality: workoutData.modality,
                focus: workoutData.focus,
                description: workoutData.description,
                structure: workoutData.structure,
                tss: workoutData.tss || 0,
                is_user_created: true,
                is_user_locked: true,
              }
            : day,
        ),
      );
    },
    [],
  );

  const editWorkout = useCallback(
    (dayIndex: number, workoutData: Partial<Workout>): void => {
      setDays((prev) =>
        prev.map((day, i) =>
          i === dayIndex
            ? {
                ...day,
                title: workoutData.title ?? day.title,
                modality: workoutData.modality ?? day.modality,
                focus: workoutData.focus ?? day.focus,
                description: workoutData.description ?? day.description,
                structure: workoutData.structure ?? day.structure,
                tss: workoutData.tss ?? day.tss,
              }
            : day,
        ),
      );
    },
    [],
  );

  const deleteWorkout = useCallback((dayIndex: number): void => {
    setDays((prev) =>
      prev.map((day, i) =>
        i === dayIndex
          ? {
              day_index: i,
              workout_id: null,
              title: null,
              modality: null,
              focus: null,
              description: null,
              structure: null,
              tss: 0,
              is_user_locked: day.is_user_locked,
            }
          : day,
      ),
    );
  }, []);

  const addRestDay = useCallback((dayIndex: number): void => {
    setDays((prev) =>
      prev.map((day, i) =>
        i === dayIndex
          ? {
              ...day,
              workout_id: `rest_${Date.now()}`,
              title: "Rest Day",
              modality: "Rest",
              focus: "Rest",
              description: "Recovery day - no training",
              structure: [],
              tss: 0,
              is_user_created: true,
              is_user_locked: true,
            }
          : day,
      ),
    );
  }, []);

  // Build workout using AI
  const buildWorkout = useCallback(
    async (
      userInputs: Partial<Workout>,
      naturalLanguagePrompt?: string,
    ): Promise<BuildWorkoutResponse> => {
      try {
        const response = await api.post("/workouts/build", {
          user_inputs: userInputs,
          natural_language_prompt: naturalLanguagePrompt,
        });

        return {
          success: true,
          workout: response.data.workout,
          generation_mode: response.data.generation_mode,
          match_confidence: response.data.match_confidence,
          errors: response.data.errors,
        };
      } catch (err: unknown) {
        console.error("Workout builder error:", err);
        const errorMessage =
          err instanceof Error ? err.message : "Unknown error";
        return {
          success: false,
          error: errorMessage,
        } as BuildWorkoutResponse;
      }
    },
    [],
  );

  return {
    days,
    cycleLength,
    setCycleLength,
    loading,
    suggestPlan,
    savePlan,
    toggleLock,
    clearPlan,
    reasoning,
    fetchLatest,
    // Plan loading
    savedPlans,
    currentPlanId,
    fetchAllPlans,
    loadPlan,
    // Workout CRUD
    addWorkout,
    editWorkout,
    deleteWorkout,
    addRestDay,
    buildWorkout,
  };
}

export default usePlanner;
