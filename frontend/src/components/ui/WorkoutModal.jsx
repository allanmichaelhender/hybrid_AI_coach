import { X, Clock, Zap, Activity, Info } from "lucide-react";

export const WorkoutModal = ({ day, isOpen, onClose }) => {
  if (!isOpen || !day) return null;

  // DEBUGGING: Remove this once you see data in the console
  console.log("Modal Data received:", day);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-zinc-900 border border-zinc-800 w-full max-w-xl rounded-3xl overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-zinc-800 flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[10px] font-black text-hybrid-neon bg-hybrid-neon/10 px-2 py-0.5 rounded uppercase tracking-widest">
                Day {(day.day_index ?? 0) + 1}
              </span>
              <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">
                {day.modality} • {day.focus}
              </span>
            </div>
            <h2 className="text-2xl font-black text-white uppercase tracking-tighter italic">
              {day.title || "Untitled Session"}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-zinc-800 rounded-full transition-colors text-zinc-500 hover:text-white"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="p-8 max-h-[65vh] overflow-y-auto custom-scrollbar">
          {/* 1. Description - Checking for common DB name variations */}
          <div className="mb-10">
            <h4 className="text-[10px] font-black text-zinc-600 uppercase tracking-widest mb-3 flex items-center gap-2">
              <Info className="w-3 h-3" /> Coach's Notes
            </h4>
            <p className="text-zinc-300 leading-relaxed font-medium">
              {day.description ||
                day.workout_description ||
                "No specific notes for this session."}
            </p>
          </div>

          {/* 2. Structure List */}
          <h4 className="text-[10px] font-black text-zinc-600 uppercase tracking-widest mb-4 flex items-center gap-2">
            <Activity className="w-3 h-3" /> Session Structure
          </h4>

          <div className="space-y-6">
            {day.structure?.map((block, blockIdx) => (
              <div key={blockIdx} className="space-y-3">
                {/* Optional: Show Block Name/Repeat if it's more than 1 */}
                <div className="flex justify-between items-center px-1">
                  <span className="text-[9px] font-black text-zinc-500 uppercase tracking-widest">
                    {block.name}{" "}
                    {block.repeat_count > 1 ? `(x${block.repeat_count})` : ""}
                  </span>
                </div>

                {block.steps?.map((step, stepIdx) => (
                  <div
                    key={stepIdx}
                    className="flex items-center justify-between p-4 bg-black/40 border border-zinc-800/50 rounded-2xl hover:border-zinc-700 transition-all"
                  >
                    <div className="flex flex-col">
                      <span className="text-[10px] font-bold text-zinc-600 mb-1">
                        PART {stepIdx + 1}
                      </span>
                      <span className="font-bold text-sm text-white">
                        {step.name}
                      </span>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="flex items-center gap-1.5 text-zinc-500">
                        <Clock className="w-3.5 h-3.5" />
                        {/* Check if it's duration_mins or duration (common DB mismatch) */}
                        <span className="text-xs font-bold">
                          {step.duration_mins || step.duration || 0}m
                        </span>
                      </div>
                      <div
                        className={`text-[10px] font-black w-12 text-center py-1 rounded ${
                          (step.intensity_factor || 0) > 0.8
                            ? "text-red-500 bg-red-500/10"
                            : "text-hybrid-neon bg-hybrid-neon/10"
                        }`}
                      >
                        {Math.round((step.intensity_factor || 0) * 100)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>

        {/* Summary Footer */}
        <div className="p-6 bg-zinc-950/50 border-t border-zinc-800 flex justify-between">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-hybrid-neon" />
            <span className="text-xs font-bold text-zinc-400 uppercase tracking-tighter">
              Estimated TSS:{" "}
              <span className="text-white">
                {day.tss || day.calculated_tss || 0}
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
