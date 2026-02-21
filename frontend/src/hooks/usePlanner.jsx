import { useState, useEffect } from "react";
import api from "../api/client";
import { useAuth } from "./useAuth";

export const usePlanner = () => {
  const { isLoggedIn } = useAuth();
  const [days, setDays] = useState([]);
  const [cycleLength, setCycleLength] = useState(7);
  const [loading, setLoading] = useState(false);
  const [reasoning, setReasoning] = useState(""); 

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
      if (response.data.coach_reasoning?.length > 0) {
        const rawReasoning =
          response.data.coach_reasoning[
            response.data.coach_reasoning.length - 1
          ];

        // ✨ PRO MOVE: Regex to remove the [0]: Modality search intents
        // This leaves only the natural language explanation for the user.
        const cleanReasoning = rawReasoning
          .replace(/\[\d+\].*?\|.*?\|.*?\n?/g, "") // Removes search intent lines
          .replace(/Search Intents:?\n?/gi, "") // Removes the header
          .trim();

        setReasoning(cleanReasoning);
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

  return {
    days,
    cycleLength,
    setCycleLength,
    loading,
    suggestPlan,
    toggleLock,
    clearPlan,
    reasoning, // 👈 Passed to Home.jsx
  };
};
