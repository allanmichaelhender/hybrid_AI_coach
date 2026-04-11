import { useState, useEffect } from "react";
import { X, Brain, Sparkles, Loader2, Check, AlertCircle } from "lucide-react";
import type {
  WorkoutEditorModalProps,
  Workout,
  Modality,
  Focus,
} from "@/types";

const MODALITIES: Modality[] = [
  "Running",
  "Cycling",
  "Swimming",
  "Strength",
  "Conditioning",
  "Hypertrophy",
  "Rest",
];
const FOCUSES: Focus[] = [
  "Aerobic Low",
  "Aerobic High",
  "VO2 Max",
  "Threshold",
  "Anaerobic",
  "Strength",
  "Hypertrophy",
  "Rest",
];

function WorkoutEditorModal({
  isOpen,
  onClose,
  dayIndex,
  day,
  onSave,
  onDelete,
  buildWorkout,
}: WorkoutEditorModalProps): React.JSX.Element | null {
  const [mode, setMode] = useState<"manual" | "ai">("manual");
  const [loading, setLoading] = useState<boolean>(false);
  const [previewWorkout, setPreviewWorkout] = useState<Workout | null>(null);
  const [generationMode, setGenerationMode] = useState<string | null>(null);
  const [matchConfidence, setMatchConfidence] = useState<number | null>(null);
  const [errors, setErrors] = useState<string[]>([]);

  // Form state
  const [title, setTitle] = useState<string>("");
  const [modality, setModality] = useState<Modality>("Running");
  const [focus, setFocus] = useState<Focus>("Aerobic Low");
  const [description, setDescription] = useState<string>("");
  const [aiPrompt, setAiPrompt] = useState<string>("");

  // Initialize form when opening
  useEffect(() => {
    if (isOpen && day) {
      setTitle(day.title || "");
      setModality(day.modality || "Running");
      setFocus(day.focus || "Aerobic Low");
      setDescription(day.description || "");
      setAiPrompt("");
      setPreviewWorkout(null);
      setErrors([]);
      setMode(day.workout_id ? "manual" : "ai");
    }
  }, [isOpen, day]);

  const handleAiGenerate = async (): Promise<void> => {
    if (!aiPrompt.trim()) return;

    setLoading(true);
    setErrors([]);

    const result = await buildWorkout({ modality, focus }, aiPrompt);

    if (result.success && result.workout) {
      setPreviewWorkout(result.workout);
      setGenerationMode(result.generation_mode || null);
      setMatchConfidence(result.match_confidence || null);
    } else {
      setErrors([result.error || "Failed to generate workout"]);
    }

    setLoading(false);
  };

  const handleManualSave = (): void => {
    if (dayIndex === null) return;

    const workoutData: Partial<Workout> = {
      title,
      modality,
      focus,
      description,
      tss: previewWorkout?.tss || 0,
      structure: previewWorkout?.structure || [],
    };

    onSave(dayIndex, workoutData as Workout);
    onClose();
  };

  const handleAcceptPreview = (): void => {
    if (previewWorkout && dayIndex !== null) {
      onSave(dayIndex, previewWorkout);
      onClose();
    }
  };

  const handleDelete = (): void => {
    if (dayIndex !== null && window.confirm("Delete this workout?")) {
      onDelete(dayIndex);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="bg-zinc-900 border border-zinc-800 w-full max-w-2xl rounded-3xl overflow-hidden shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="p-6 border-b border-zinc-800 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-black text-white uppercase tracking-tighter">
              {day?.workout_id ? "Edit Workout" : "Add Workout"}
            </h2>
            <p className="text-zinc-500 text-xs mt-1">
              Day {dayIndex != null ? dayIndex + 1 : "?"}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-zinc-800 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-zinc-400" />
          </button>
        </div>

        {/* Mode Toggle */}
        <div className="px-6 py-4 border-b border-zinc-800">
          <div className="flex bg-zinc-800 p-1 rounded-xl">
            <button
              onClick={() => setMode("manual")}
              className={`flex-1 px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                mode === "manual"
                  ? "bg-zinc-700 text-white"
                  : "text-zinc-500 hover:text-white"
              }`}
            >
              Manual Entry
            </button>
            <button
              onClick={() => setMode("ai")}
              className={`flex-1 px-4 py-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-2 ${
                mode === "ai"
                  ? "bg-hybrid-neon text-black"
                  : "text-zinc-500 hover:text-white"
              }`}
            >
              <Brain className="w-3.5 h-3.5" />
              AI Assist
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {mode === "manual" ? (
            // Manual Entry Form
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                  Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Morning Tempo Run"
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                    Modality
                  </label>
                  <select
                    value={modality}
                    onChange={(e) => setModality(e.target.value as Modality)}
                    className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none"
                  >
                    {MODALITIES.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                    Focus
                  </label>
                  <select
                    value={focus}
                    onChange={(e) => setFocus(e.target.value as Focus)}
                    className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none"
                  >
                    {FOCUSES.map((f) => (
                      <option key={f} value={f}>
                        {f}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                  Description
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  placeholder="Brief description of the workout..."
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none resize-none"
                />
              </div>
            </div>
          ) : (
            // AI Assist Form
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                    Preferred Modality
                  </label>
                  <select
                    value={modality}
                    onChange={(e) => setModality(e.target.value as Modality)}
                    className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none"
                  >
                    {MODALITIES.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                    Preferred Focus
                  </label>
                  <select
                    value={focus}
                    onChange={(e) => setFocus(e.target.value as Focus)}
                    className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none"
                  >
                    {FOCUSES.map((f) => (
                      <option key={f} value={f}>
                        {f}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-2 block">
                  Describe what you want
                </label>
                <textarea
                  value={aiPrompt}
                  onChange={(e) => setAiPrompt(e.target.value)}
                  rows={3}
                  placeholder="e.g., 45 minute tempo run with a warm up and cool down..."
                  className="w-full bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white focus:border-hybrid-neon focus:outline-none resize-none"
                />
              </div>

              <button
                onClick={handleAiGenerate}
                disabled={loading || !aiPrompt.trim()}
                className="w-full py-3 bg-hybrid-neon text-black font-bold rounded-xl hover:bg-hybrid-neon/90 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Sparkles className="w-4 h-4" />
                )}
                {loading ? "Generating..." : "Generate Workout"}
              </button>

              {/* Preview */}
              {previewWorkout && (
                <div className="mt-4 p-4 bg-zinc-800/50 border border-zinc-700 rounded-xl">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-bold text-white">
                      {previewWorkout.title}
                    </h3>
                    {generationMode === "rag_match" && matchConfidence && (
                      <span className="text-xs font-bold text-hybrid-neon bg-hybrid-neon/10 px-2 py-1 rounded">
                        DB Match ({Math.round(matchConfidence * 100)}%)
                      </span>
                    )}
                    {generationMode === "synthetic" && (
                      <span className="text-xs font-bold text-blue-400 bg-blue-400/10 px-2 py-1 rounded">
                        AI Generated
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-zinc-400 mb-3">
                    {previewWorkout.description}
                  </p>
                  <div className="flex gap-3 text-xs">
                    <span className="bg-zinc-700 px-2 py-1 rounded text-zinc-300">
                      {previewWorkout.modality}
                    </span>
                    <span className="bg-zinc-700 px-2 py-1 rounded text-zinc-300">
                      {previewWorkout.focus}
                    </span>
                    <span className="bg-zinc-700 px-2 py-1 rounded text-hybrid-neon">
                      {Math.round(previewWorkout.tss)} TSS
                    </span>
                  </div>
                </div>
              )}

              {errors.length > 0 && (
                <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-red-500" />
                  <span className="text-sm text-red-400">{errors[0]}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="p-6 border-t border-zinc-800 flex justify-between">
          {day?.workout_id && (
            <button
              onClick={handleDelete}
              className="text-red-500 hover:text-red-400 text-sm font-bold px-4 py-2"
            >
              Delete
            </button>
          )}

          <div className="flex gap-3 ml-auto">
            <button
              onClick={onClose}
              className="px-4 py-2 text-zinc-400 hover:text-white text-sm font-bold"
            >
              Cancel
            </button>

            {mode === "ai" && previewWorkout ? (
              <button
                onClick={handleAcceptPreview}
                className="px-6 py-2 bg-hybrid-neon text-black font-bold rounded-xl hover:bg-hybrid-neon/90 transition-all flex items-center gap-2"
              >
                <Check className="w-4 h-4" />
                Add to Calendar
              </button>
            ) : (
              <button
                onClick={handleManualSave}
                disabled={!title.trim()}
                className="px-6 py-2 bg-hybrid-neon text-black font-bold rounded-xl hover:bg-hybrid-neon/90 transition-all disabled:opacity-50"
              >
                {day?.workout_id ? "Save Changes" : "Add Workout"}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default WorkoutEditorModal;
