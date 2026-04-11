import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import usePlanner from "../hooks/usePlanner";
import DayCard from "../components/ui/DayCard";
import Button from "../components/ui/Button";
import WorkoutModal from "../components/ui/WorkoutModal";
import WorkoutEditorModal from "../components/ui/WorkoutEditorModal";
import PlanSelector from "../components/ui/PlanSelector";
import {
  Zap,
  LogOut,
  LogIn,
  Trash2,
  Sparkles,
  Loader2,
  Activity,
  Calendar,
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import type { CalendarDay, Workout } from "@/types";

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function Home(): React.JSX.Element {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  // 1. Pull everything from our custom hook (including reasoning)
  const {
    days,
    cycleLength,
    setCycleLength,
    loading,
    suggestPlan,
    toggleLock,
    clearPlan,
    reasoning,
    savePlan,
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
  } = usePlanner();

  const [goal, setGoal] = useState<string>(
    `Example: Focus on aerobic threshold running. Have my high intensity running days on Monday and Thursday.
    
I want my strength sessions to be on Tuesdays and Fridays. Wednesday as my rest day. Cycling is the best form of low intensity training for me add this on the remaining days.`,
  );
  const [selectedDay, setSelectedDay] = useState<CalendarDay | null>(null);
  const [editingDayIndex, setEditingDayIndex] = useState<number | null>(null);
  const [showPlanSelector, setShowPlanSelector] = useState<boolean>(false);

  // Calculate TSS metrics
  const currentDays = days.slice(0, cycleLength);
  const totalTss = currentDays.reduce((sum, day) => sum + (day.tss || 0), 0);
  const avgTss =
    currentDays.length > 0 ? Math.round(totalTss / currentDays.length) : 0;

  // Weekly breakdown
  const weeklyTss: number[] = [];
  for (let i = 0; i < currentDays.length; i += 7) {
    const week = currentDays.slice(i, i + 7);
    weeklyTss.push(week.reduce((sum, day) => sum + (day.tss || 0), 0));
  }

  // Build weeks for display
  const weeks: CalendarDay[][] = [];
  for (let i = 0; i < currentDays.length; i += 7) {
    weeks.push(currentDays.slice(i, i + 7));
  }

  return (
    <div className="min-h-screen bg-black text-white selection:bg-hybrid-neon selection:text-black">
      {/* --- 1. TOP NAVIGATION (Unchanged) --- */}
      <nav className="border-b border-zinc-900 p-4 sticky top-0 bg-black/80 backdrop-blur-md z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-hybrid-neon rounded-lg flex items-center justify-center">
              <Zap className="text-black w-5 h-5" />
            </div>
            <span className="font-black tracking-tighter text-xl uppercase">
              Hybrid Hour
            </span>
          </div>

          <div className="flex items-center gap-4">
            {isLoggedIn && (
              <PlanSelector
                isOpen={false}
                onClose={() => {}}
                plans={savedPlans}
                currentPlanId={currentPlanId}
                onLoadPlan={loadPlan}
                onFetchPlans={fetchAllPlans}
                loading={loading}
              />
            )}
            {isLoggedIn ? (
              <Button
                variant="outline"
                onClick={logout}
                className="gap-2 text-xs"
              >
                <LogOut className="w-3.5 h-3.5" /> Logout
              </Button>
            ) : (
              <Button
                variant="primary"
                onClick={() => navigate("/login")}
                className="gap-2 text-xs py-2"
              >
                <LogIn className="w-3.5 h-3.5" /> Sign In
              </Button>
            )}
          </div>
        </div>
      </nav>

      <main className="p-8 pt-2 max-w-[95vw] mx-auto">
        {/* --- 2. HEADER & CYCLE TOGGLE --- */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-6">
          <div className="flex items-center gap-8">
            <h2 className="text-3xl font-black uppercase tracking-tighter">
              <span className="text-hybrid-neon">TRAINING</span> BLOCK
            </h2>
            {/* TSS Metrics Summary */}
            <div className="flex items-center gap-4 text-xs">
              <span className="text-zinc-500">
                Total:{" "}
                <span className="text-hybrid-neon font-bold">
                  {Math.round(totalTss)} TSS
                </span>
              </span>
              <span className="text-zinc-600">|</span>
              <span className="text-zinc-500">
                Avg: <span className="text-white font-bold">{avgTss}/day</span>
              </span>
              {weeklyTss.map((weekTss, idx) => (
                <React.Fragment key={idx}>
                  <span className="text-zinc-600">|</span>
                  <span className="text-zinc-500">
                    W{idx + 1}:{" "}
                    <span className="text-white font-bold">
                      {Math.round(weekTss)}
                    </span>
                  </span>
                </React.Fragment>
              ))}
            </div>
          </div>

          <div className="flex items-center gap-3 self-start md:self-end">
            <button
              onClick={clearPlan}
              className="text-red-800 hover:text-red-500 flex items-center gap-2 text-xs font-bold transition-colors"
            >
              <Trash2 className="w-4 h-4" /> RESET
            </button>
            <div className="flex bg-zinc-900 p-1 rounded-xl border border-zinc-800">
              {[7, 14].map((len) => (
                <button
                  key={len}
                  onClick={() => setCycleLength(len)}
                  className={`px-6 py-2 rounded-lg font-bold text-xs transition-all ${cycleLength === len ? "bg-hybrid-neon text-black" : "text-zinc-500 hover:text-white"}`}
                >
                  {len} DAYS
                </button>
              ))}
            </div>
            {isLoggedIn && (
              <Button
                variant="outline"
                onClick={() => setShowPlanSelector(true)}
                className="gap-2 text-xs py-2 border-zinc-700 hover:border-hybrid-neon/30"
              >
                <Calendar className="w-3.5 h-3.5" />
                MY PLANS
              </Button>
            )}
            {isLoggedIn && (
              <Button
                variant="outline"
                onClick={() => savePlan(goal)}
                disabled={loading || days.every((d) => !d.workout_id)}
                className="gap-2 text-xs py-2 border-hybrid-neon/20 hover:border-hybrid-neon/50 transition-all hover:bg-hybrid-neon/5"
              >
                <Sparkles className="w-3.5 h-3.5 text-hybrid-neon" />
                SAVE
              </Button>
            )}
          </div>
        </div>

        {/* --- 3. MAIN CONTENT AREA (Calendar + Prompt + Coach Logic) --- */}
        <div className="flex flex-col lg:flex-row gap-8 mb-12">
          {/* --- LEFT: CALENDAR GRID (3/5) --- */}
          <div className="lg:w-3/5 space-y-12">
            {weeks.map((week, weekIdx) => (
              <div
                key={weekIdx}
                className="animate-in fade-in slide-in-from-bottom-4 duration-500"
              >
                {/* Week Header Line */}
                <div className="flex items-center gap-4 mb-6 opacity-40">
                  <span className="text-[10px] font-black uppercase tracking-[0.4em] whitespace-nowrap">
                    Week {weekIdx + 1}
                  </span>
                  <div className="h-[1px] w-full bg-zinc-800" />
                </div>

                <div className="grid grid-cols-2 min-[1080px]:grid-cols-3 min-[1340px]:grid-cols-4 min-[1620px]:grid-cols-5 gap-4">
                  {week.map((day) => (
                    <div key={day.day_index} className="flex flex-col gap-2">
                      {/* WEEKDAY LABEL */}
                      <div className="flex justify-between items-center px-1">
                        <span className="text-[10px] font-black text-white uppercase tracking-widest">
                          {WEEKDAYS[day.day_index % 7]}
                        </span>
                        <span className="text-[9px] font-bold text-zinc-700">
                          DAY {day.day_index + 1}
                        </span>
                      </div>

                      <DayCard
                        day={day}
                        onToggleLock={toggleLock}
                        onClick={() => day.workout_id && setSelectedDay(day)}
                        onEdit={(idx) => setEditingDayIndex(idx)}
                        onRestDay={addRestDay}
                        onDelete={deleteWorkout}
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* --- RIGHT: PROMPT BOX + COACH LOGIC (2/5) --- */}
          <div className="lg:w-2/5 flex flex-col gap-8">
            {/* --- 4. EXPANDED AI MISSION INPUT --- */}
            <div className="bg-zinc-900/40 border border-zinc-800 p-2 rounded-2xl transition-all focus-within:border-hybrid-neon/30 shadow-2xl">
              <textarea
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                rows={4}
                onInput={(e) => {
                  e.currentTarget.style.height = "auto";
                  e.currentTarget.style.height =
                    e.currentTarget.scrollHeight + "px";
                }}
                className="w-full bg-transparent px-4 py-3 focus:outline-none text-sm font-medium text-zinc-200 placeholder:text-zinc-700 resize-none leading-relaxed min-h-[120px] max-h-[400px]"
              />

              {/* Compact Action Bar (Streamlined) */}
              <div className="flex justify-between items-center px-2 py-1.5 border-t border-zinc-800/50 mt-1">
                <div className="flex items-center gap-2 text-[10px] font-black text-zinc-600 uppercase tracking-widest pl-2">
                  <Zap className="w-3 h-3 opacity-50" />
                  Powered by Llama 3.3
                </div>

                <Button
                  onClick={() => suggestPlan(goal)}
                  disabled={loading || !goal.trim()}
                  className="h-8 px-5 rounded-lg text-[10px] tracking-[0.2em] font-black bg-hybrid-neon text-black hover:bg-hybrid-neon/90 transition-all"
                >
                  {loading ? (
                    <Loader2 className="animate-spin w-3 h-3" />
                  ) : (
                    <Sparkles className="w-3 h-3 fill-current" />
                  )}
                  GENERATE PLAN
                </Button>
              </div>
            </div>

            {/* --- 5. COACH'S LOGIC (AI REASONING) --- */}
            {reasoning && (
              <div className="animate-in fade-in slide-in-from-bottom-6 duration-1000">
                <div className="bg-zinc-900/30 border border-zinc-800 rounded-3xl p-6 backdrop-blur-sm relative overflow-hidden group">
                  <div className="absolute -right-20 -top-20 w-64 h-64 bg-hybrid-neon/5 blur-[100px] rounded-full" />
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-10 h-10 bg-hybrid-neon/10 rounded-2xl flex items-center justify-center border border-hybrid-neon/20 shadow-inner">
                      <Activity className="text-hybrid-neon w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-black text-white uppercase tracking-tighter text-lg">
                        Coach's <span className="text-hybrid-neon">Logic</span>
                      </h3>
                      <p className="text-zinc-500 text-[10px] font-black uppercase tracking-[0.2em] leading-none">
                        Automated Analysis
                      </p>
                    </div>
                  </div>
                  <div className="relative">
                    <p className="text-zinc-300 leading-relaxed text-sm font-medium whitespace-pre-line italic border-l-2 border-hybrid-neon/30 pl-6">
                      {reasoning}
                    </p>
                  </div>
                  <div className="mt-6 flex items-center gap-3 text-[10px] font-black text-zinc-700 uppercase tracking-[0.2em]">
                    <div className="w-1.5 h-1.5 bg-hybrid-neon rounded-full animate-pulse shadow-[0_0_8px_#ccff00]" />
                    Llama 3.3 Engine
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <WorkoutModal
        day={selectedDay}
        isOpen={!!selectedDay}
        onClose={() => setSelectedDay(null)}
      />

      <WorkoutEditorModal
        isOpen={editingDayIndex !== null}
        onClose={() => setEditingDayIndex(null)}
        dayIndex={editingDayIndex}
        day={editingDayIndex !== null ? days[editingDayIndex] : null}
        onSave={(idx: number, data: Workout) => {
          if (days[idx]?.workout_id) {
            editWorkout(idx, data);
          } else {
            addWorkout(idx, data);
          }
          setEditingDayIndex(null);
        }}
        onDelete={(idx: number) => {
          deleteWorkout(idx);
          setEditingDayIndex(null);
        }}
        buildWorkout={buildWorkout}
      />

      <PlanSelector
        isOpen={showPlanSelector}
        onClose={() => setShowPlanSelector(false)}
        plans={savedPlans}
        currentPlanId={currentPlanId}
        onLoadPlan={loadPlan}
        onFetchPlans={fetchAllPlans}
        loading={loading}
      />
    </div>
  );
}

export default Home;
