import { useState, useEffect } from 'react';
import api from '../api/client';
import { useAuth } from './useAuth';

export const usePlanner = () => {
  const { isLoggedIn } = useAuth();
  const [days, setDays] = useState([]);
  const [cycleLength, setCycleLength] = useState(7);
  const [loading, setLoading] = useState(false);

  // 1. INITIALIZATION: Load data based on Auth Status
  useEffect(() => {
    const savedGuestPlan = localStorage.getItem('guest_plan');
    
    if (!isLoggedIn && savedGuestPlan) {
      // If Guest: Load their local draft
      setDays(JSON.parse(savedGuestPlan));
    } else {
      // If Logged In: We'll eventually fetch from /api/v1/calendar/
      // For now, initialize a clean 14-day slate
      setDays(Array.from({ length: 14 }, (_, i) => ({
        day_index: i,
        workout_id: null,
        title: null,
        modality: null,
        focus: null,
        tss: 0,
        is_user_locked: false
      })));
    }
  }, [isLoggedIn]);

  // 2. GUEST PERSISTENCE: Save to localStorage whenever days change
  useEffect(() => {
    if (!isLoggedIn && days.length > 0) {
      localStorage.setItem('guest_plan', JSON.stringify(days));
    }
  }, [days, isLoggedIn]);

  // 3. THE AI ORCHESTRATOR: Call the LangGraph Agent
  const suggestPlan = async (userGoal) => {
    setLoading(true);
    try {
      const response = await api.post('/calendar/suggest', {
        calendar: days.slice(0, cycleLength),
        user_goal: userGoal,
        cycle_length: cycleLength,
        request_scope: "bulk"
      });

      // Merge the AI's 7 or 14 day suggestion back into our 14-day state
      const updated = [...days];
      response.data.updated_calendar.forEach(d => {
        updated[d.day_index] = d;
      });
      setDays(updated);
      return { success: true };
    } catch (err) {
      console.error("AI Planner Error:", err);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  // 4. THE STATE MODIFIERS
  const toggleLock = (idx) => {
    setDays(prev => prev.map((day, i) => 
      i === idx ? { ...day, is_user_locked: !day.is_user_locked } : day
    ));
  };

  const clearPlan = () => {
    if (window.confirm("Are you sure you want to clear your current plan?")) {
      setDays(Array.from({ length: 14 }, (_, i) => ({
        day_index: i, workout_id: null, is_user_locked: false, tss: 0
      })));
    }
  };

  return { 
    days, 
    cycleLength, 
    setCycleLength, 
    loading, 
    suggestPlan, 
    toggleLock,
    clearPlan
  };
};
