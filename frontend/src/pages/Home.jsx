import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { usePlanner } from '../hooks/usePlanner';
import { DayCard } from '../features/planner/components/DayCard';
import { Button } from '../components/ui/Button';
import { 
  Brain, 
  LogOut, 
  LogIn, 
  Trash2, 
  Sparkles, 
  Loader2, 
  ChevronRight 
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();
  
  // 1. Pull everything from our custom "Brain" hook
  const { 
    days, 
    cycleLength, 
    setCycleLength, 
    loading, 
    suggestPlan, 
    toggleLock,
    clearPlan 
  } = usePlanner();

  const [goal, setGoal] = useState("Focus on VO2 Max and Strength");

  return (
    <div className="min-h-screen bg-black text-white selection:bg-hybrid-neon selection:text-black">
      {/* 1. TOP NAVIGATION */}
      <nav className="border-b border-zinc-900 p-4 sticky top-0 bg-black/80 backdrop-blur-md z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-hybrid-neon rounded-lg flex items-center justify-center">
              <Brain className="text-black w-5 h-5" />
            </div>
            <span className="font-black tracking-tighter text-xl uppercase">Hybrid Hour</span>
          </div>
          
          <div className="flex items-center gap-4">
            {isLoggedIn ? (
              <Button variant="outline" onClick={logout} className="gap-2 text-xs">
                <LogOut className="w-3.5 h-3.5" /> Logout
              </Button>
            ) : (
              <Button variant="primary" onClick={() => navigate('/login')} className="gap-2 text-xs py-2">
                <LogIn className="w-3.5 h-3.5" /> Sign In
              </Button>
            )}
          </div>
        </div>
      </nav>

      <main className="p-8 max-w-7xl mx-auto">
        {/* 2. HEADER & TOGGLE */}
        <div className="flex flex-col md:flex-row justify-between items-end mb-10 gap-6">
          <div>
            <h2 className="text-4xl font-black mb-2 uppercase tracking-tighter">Your Training <span className="text-hybrid-neon">Block</span></h2>
            <p className="text-zinc-500 font-medium italic">Adaptive 60-minute sessions via Llama 3.1</p>
          </div>

          <div className="flex bg-zinc-900 p-1 rounded-xl border border-zinc-800 self-start md:self-end">
            {[7, 14].map(len => (
              <button key={len} onClick={() => setCycleLength(len)}
                className={`px-6 py-2 rounded-lg font-bold text-xs transition-all ${cycleLength === len ? 'bg-hybrid-neon text-black' : 'text-zinc-500 hover:text-white'}`}>
                {len} DAYS
              </button>
            ))}
          </div>
        </div>

        {/* 3. AI INPUT SECTION */}
        <div className="bg-zinc-900/40 border border-zinc-800 p-3 rounded-2xl mb-12 flex flex-col md:flex-row gap-3">
          <input 
            value={goal} 
            onChange={(e) => setGoal(e.target.value)}
            className="flex-1 bg-transparent px-5 py-3 focus:outline-none text-lg font-bold placeholder:text-zinc-800"
            placeholder="What's the training objective?" 
          />
          <Button onClick={() => suggestPlan(goal)} disabled={loading} className="py-4 md:px-10">
            {loading ? <Loader2 className="animate-spin w-5 h-5" /> : <Sparkles className="w-5 h-5" />}
            GENERATE PLAN
          </Button>
        </div>

        {/* 4. THE CALENDAR GRID */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7 gap-4 mb-12">
          {days.slice(0, cycleLength).map((day, idx) => (
            <DayCard 
              key={idx} 
              day={day} 
              onToggleLock={toggleLock} 
            />
          ))}
        </div>

        {/* 5. FOOTER ACTIONS */}
        <div className="flex justify-between items-center pt-8 border-t border-zinc-900">
          <button onClick={clearPlan} className="text-zinc-700 hover:text-red-500 flex items-center gap-2 text-xs font-bold transition-colors">
            <Trash2 className="w-4 h-4" /> RESET DRAFT
          </button>
          
          {!isLoggedIn && (
            <p className="text-zinc-600 text-[10px] uppercase font-bold tracking-widest">
              Guest Mode • <button onClick={() => navigate('/register')} className="text-hybrid-neon hover:underline">Register to sync profile</button>
            </p>
          )}
        </div>
      </main>
    </div>
  );
}

export default Home;
