import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { usePlanner } from "../hooks/usePlanner";
import { DayCard } from "../components/ui/DayCard";
import { Button } from "../components/ui/Button";
import { WorkoutModal } from "../components/ui/WorkoutModal";
import { addDays, format } from "date-fns";
import {
  Brain,
  LogOut,
  LogIn,
  Trash2,
  Sparkles,
  Loader2,
  Info,
  Activity,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function Home() {
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
    fetchLatest,
  } = usePlanner();

  const [goal, setGoal] = useState(
    `Example: Focus on running aerobic threshold traiing with regular low intensity days. 

Have my high intensity running days on Monday and Wednesdays, Cycling is the best form of low intensity training for me.

I want to do at least two Hypertrophy sessions too per week.`,
  );
  const [selectedDay, setSelectedDay] = useState(null);

  const currentDays = days.slice(0, cycleLength);
  const weeks = [];
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
              <Brain className="text-black w-5 h-5" />
            </div>
            <span className="font-black tracking-tighter text-xl uppercase">
              Hybrid Hour
            </span>
          </div>

          <div className="flex items-center gap-4">
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

      <main className="p-8 max-w-7xl mx-auto">
        {/* --- 2. HEADER & CYCLE TOGGLE (Unchanged) --- */}
        <div className="flex flex-col md:flex-row justify-between items-end mb-10 gap-6">
          <div>
            <h2 className="text-4xl font-black mb-2 uppercase tracking-tighter">
              Your Training <span className="text-hybrid-neon">Block</span>
            </h2>
          </div>

          <div className="flex bg-zinc-900 p-1 rounded-xl border border-zinc-800 self-start md:self-end">
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
        </div>

        {/* --- 3. EXPANDED AI MISSION INPUT --- */}
        <div className="bg-zinc-900/40 border border-zinc-800 p-2 rounded-2xl mb-12 transition-all focus-within:border-hybrid-neon/30 shadow-2xl">
          <textarea
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            // 🚀 THE FIX: Increase initial rows and min-height
            rows={4}
            onInput={(e) => {
              e.target.style.height = "auto";
              e.target.style.height = e.target.scrollHeight + "px";
            }}
            // Added 'min-h-[120px]' for a much larger starting presence
            className="w-full bg-transparent px-4 py-3 focus:outline-none text-sm font-medium text-zinc-200 placeholder:text-zinc-700 resize-none leading-relaxed min-h-[120px] max-h-[400px]"
          />

          {/* Compact Action Bar (Streamlined) */}
          <div className="flex justify-between items-center px-2 py-1.5 border-t border-zinc-800/50 mt-1">
            <div className="flex items-center gap-2 text-[10px] font-black text-zinc-600 uppercase tracking-widest pl-2">
              <Brain className="w-3 h-3 opacity-50" />
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

        {/* --- 4. THE CHUNKED CALENDAR GRID (NEW LOGIC) --- */}
        <div className="space-y-12 mb-12">
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

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7 gap-4">
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
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* --- 6. FOOTER ACTIONS (Unchanged) --- */}
        <div className="flex justify-between items-center mt-12 pt-8 border-t border-zinc-900">
          <button
            onClick={clearPlan}
            className="text-zinc-700 hover:text-red-500 flex items-center gap-2 text-xs font-bold transition-colors"
          >
            <Trash2 className="w-4 h-4" /> RESET WORKOUT PLAN
          </button>

          <div className="flex items-center gap-4">
            {!isLoggedIn ? (
              <p className="text-zinc-600 text-[10px] uppercase font-bold tracking-widest">
                Guest Mode •{" "}
                <button
                  onClick={() => navigate("/register")}
                  className="text-hybrid-neon hover:underline"
                >
                  LOGIN TO SAVE PLAN
                </button>
              </p>
            ) : (
              // 🚀 THE NEW CLOUD SYNC BUTTON
              <Button
                variant="outline"
                onClick={() => savePlan(goal)}
                disabled={loading || days.every((d) => !d.workout_id)}
                className="gap-2 text-xs py-2 border-hybrid-neon/20 hover:border-hybrid-neon/50 transition-all hover:bg-hybrid-neon/5"
              >
                <Sparkles className="w-3.5 h-3.5 text-hybrid-neon" />
                SAVE TO CLOUD
              </Button>
            )}
          </div>
        </div>

        {/* --- 7. COACH'S LOGIC (AI REASONING) (Unchanged) --- */}
        {reasoning && (
          <div className="mt-12 animate-in fade-in slide-in-from-bottom-6 duration-1000">
            <div className="bg-zinc-900/30 border border-zinc-800 rounded-3xl p-8 backdrop-blur-sm relative overflow-hidden group">
              <div className="absolute -right-20 -top-20 w-64 h-64 bg-hybrid-neon/5 blur-[100px] rounded-full" />
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-hybrid-neon/10 rounded-2xl flex items-center justify-center border border-hybrid-neon/20 shadow-inner">
                  <Activity className="text-hybrid-neon w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-black text-white uppercase tracking-tighter text-xl">
                    Coach's <span className="text-hybrid-neon">Logic</span>
                  </h3>
                  <p className="text-zinc-500 text-[10px] font-black uppercase tracking-[0.2em] leading-none">
                    Automated Neural Analysis
                  </p>
                </div>
              </div>
              <div className="relative">
                <p className="text-zinc-300 leading-relaxed text-lg font-medium whitespace-pre-line italic border-l-2 border-hybrid-neon/30 pl-8">
                  {reasoning}
                </p>
              </div>
              <div className="mt-8 flex items-center gap-3 text-[10px] font-black text-zinc-700 uppercase tracking-[0.2em]">
                <div className="w-1.5 h-1.5 bg-hybrid-neon rounded-full animate-pulse shadow-[0_0_8px_#ccff00]" />
                Llama 3.3 Reasoning Engine Active
              </div>
            </div>
          </div>
        )}
      </main>

      <WorkoutModal
        day={selectedDay}
        isOpen={!!selectedDay}
        onClose={() => setSelectedDay(null)}
      />
    </div>
  );
}

export default Home;
