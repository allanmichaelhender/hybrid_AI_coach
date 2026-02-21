// src/components/ui/DayCard.jsx
import { Lock, Unlock, Zap } from 'lucide-react';

export const DayCard = ({ day, onToggleLock }) => {
  const hasWorkout = !!day.workout_id;

  return (
    <div className={`relative min-h-[180px] p-5 rounded-2xl border transition-all duration-500 ${
      hasWorkout 
        ? 'bg-zinc-900 border-zinc-700 shadow-xl' 
        : 'bg-transparent border-dashed border-zinc-800 hover:border-zinc-700'
    }`}>
      {/* Day Header */}
      <div className="flex justify-between items-center mb-6">
        <span className="text-[10px] font-black text-zinc-600 tracking-[0.2em] uppercase">
          Day {day.day_index + 1}
        </span>
        <button 
          onClick={() => onToggleLock(day.day_index)} 
          className="transition-colors hover:text-hybrid-neon group"
        >
          {day.is_user_locked ? (
            <Lock className="w-4 h-4 text-hybrid-neon" />
          ) : (
            <Unlock className="w-4 h-4 text-zinc-800 group-hover:text-zinc-600" />
          )}
        </button>
      </div>

      {/* Content */}
      {hasWorkout ? (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
          <h3 className="font-bold text-sm leading-tight mb-4 h-10 line-clamp-2 text-white">
            {day.title}
          </h3>
          <div className="flex items-center gap-2">
            <span className="text-[9px] font-black bg-zinc-800 text-zinc-400 px-2 py-1 rounded tracking-widest uppercase">
              {day.modality}
            </span>
            <div className="flex items-center gap-1 text-hybrid-neon">
              <Zap className="w-3 h-3 fill-current" />
              <span className="text-[9px] font-black tracking-widest">{day.tss} TSS</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="h-full flex items-center justify-center opacity-5">
          <Zap className="w-8 h-8 text-white" />
        </div>
      )}
    </div>
  );
};
