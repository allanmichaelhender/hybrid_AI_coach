import { useState, useEffect, useCallback } from "react";
import api from "../api/client";
import { useAuth } from "./useAuth";

export const usePlanner = () => {
  const { isLoggedIn } = useAuth();
  const [days, setDays] = useState([]);
  const [cycleLength, setCycleLength] = useState(7);
  const [loading, setLoading] = useState(false);
  const [reasoning, setReasoning] = useState("");

  const fetchLatest = useCallback(async () => {
    if (!isLoggedIn) return;

    setLoading(true);
    try {
      const { data } = await api.get("/calendar/latest");

      if (data && data.calendar_data) {
        // 🚀 THE MAGIC: Overwrite the local state with the Neon data
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

  // 1. INITIALIZATION: Load data based on Auth Status
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

  // 2. GUEST PERSISTENCE
  useEffect(() => {
    if (!isLoggedIn && days.length > 0) {
      localStorage.setItem("guest_plan", JSON.stringify(days));
    }
  }, [days, isLoggedIn]);

  // 3. THE AI ORCHESTRATOR
  const suggestPlan = async (userGoal) => {
    setLoading(true);
    try {
      const response = await api.post("/calendar/suggest", {
        calendar: days.slice(0, cycleLength),
        user_goal: userGoal,
        cycle_length: cycleLength,
        request_scope: "bulk",
      });

      // A. Update the Calendar State (Deep Merge)
      const newCalendar = days.map((existingDay) => {
        const aiUpdatedDay = response.data.updated_calendar.find(
          (d) => d.day_index === existingDay.day_index,
        );
        return aiUpdatedDay ? { ...existingDay, ...aiUpdatedDay } : existingDay;
      });
      setDays(newCalendar);

      // B. Capture & Format Reasoning
      if (response.data.coach_reasoning) {
    
        setReasoning(response.data.coach_reasoning);
      }

      return { success: true };
    } catch (err) {
      console.error("AI Planner Error:", err);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  const toggleLock = (idx) => {
    setDays((prev) =>
      prev.map((day, i) =>
        i === idx ? { ...day, is_user_locked: !day.is_user_locked } : day,
      ),
    );
  };

  const clearPlan = () => {
    if (window.confirm("Are you sure you want to clear your current plan?")) {
      setDays(
        Array.from({ length: 14 }, (_, i) => ({
          day_index: i,
          workout_id: null,
          is_user_locked: false,
          tss: 0,
        })),
      );
      setReasoning("");
    }
  };

  const savePlan = async (userGoal) => {
    if (!isLoggedIn) {
      alert("Sign in to save your plan to the cloud! 🚀");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        plan_name: `Mission: ${userGoal}`,
        user_goal: userGoal,
        // Match the backend Pydantic schema key:
        calendar_data: days,
        coach_reasoning: reasoning,
      };

      // Ensure the path matches your FastAPI router prefix
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
    fetchLatest // 👈 Passed to Home.jsx
  };
};
