// src/components/ui/WorkoutModal.jsx
import { X, Clock, Zap, Activity, Info } from 'lucide-react';

export const WorkoutModal = ({ day, isOpen, onClose }) => {
  if (!isOpen || !day) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-zinc-900 border border-zinc-800 w-full max-w-xl rounded-3xl overflow-hidden shadow-2xl">
        
        {/* Header */}
        <div className="p-6 border-b border-zinc-800 flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2 mb-2">
               <span className="text-[10px] font-black text-hybrid-neon bg-hybrid-neon/10 px-2 py-0.5 rounded uppercase tracking-widest">
                 Day {day.day_index + 1}
               </span>
               <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">
                 {day.modality} • {day.focus}
               </span>
            </div>
            <h2 className="text-2xl font-black text-white uppercase tracking-tighter italic">{day.title}</h2>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-zinc-800 rounded-full transition-colors text-zinc-500 hover:text-white">
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="p-8 max-h-[65vh] overflow-y-auto custom-scrollbar">
          {/* 1. Description */}
          <div className="mb-10">
            <h4 className="text-[10px] font-black text-zinc-600 uppercase tracking-widest mb-3 flex items-center gap-2">
              <Info className="w-3 h-3" /> Coach's Notes
            </h4>
            <p className="text-zinc-300 leading-relaxed font-medium">
              {day.description || "No description provided for this session."}
            </p>
          </div>

          {/* 2. Structure List */}
          <h4 className="text-[10px] font-black text-zinc-600 uppercase tracking-widest mb-4 flex items-center gap-2">
            <Activity className="w-3 h-3" /> Session Structure
          </h4>
          
          <div className="space-y-3">
            {day.structure?.map((step, i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-black/40 border border-zinc-800/50 rounded-2xl hover:border-zinc-700 transition-all">
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-zinc-600 mb-1">STEP {i + 1}</span>
                  <span className="font-bold text-sm text-white">{step.name}</span>
                </div>
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-1.5 text-zinc-500">
                    <Clock className="w-3.5 h-3.5" />
                    <span className="text-xs font-bold">{step.duration_mins}m</span>
                  </div>
                  <div className={`text-[10px] font-black w-12 text-center py-1 rounded ${
                    step.intensity_factor > 0.8 ? 'text-red-500 bg-red-500/10' : 'text-hybrid-neon bg-hybrid-neon/10'
                  }`}>
                    {Math.round(step.intensity_factor * 100)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Summary Footer */}
        <div className="p-6 bg-zinc-950/50 border-t border-zinc-800 flex justify-between">
           <div className="flex items-center gap-2">
             <Zap className="w-4 h-4 text-hybrid-neon" />
             <span className="text-xs font-bold text-zinc-400">ESTIMATED TSS: <span className="text-white">{day.tss}</span></span>
           </div>
        </div>
      </div>
    </div>
  );
};
