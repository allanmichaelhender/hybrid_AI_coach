import {
  Lock,
  Unlock,
  Zap,
  Plus,
  Edit3,
  BatteryCharging,
  Dumbbell,
  Bike,
  Waves,
  Activity,
  Timer,
  Trash2,
} from "lucide-react";
import type { ReactElement } from "react";
import type { CalendarDay, WorkoutBlock } from "@/types";

interface DayCardProps {
  day: CalendarDay;
  onToggleLock: (index: number) => void;
  onClick: () => void;
  onEdit: (index: number) => void;
  onRestDay?: (index: number) => void;
  onDelete?: (index: number) => void;
}

// Rest day detection
const isRestDay = (day: CalendarDay): boolean => {
  return day.modality === "Rest" || (day.focus === "Rest" && day.tss === 0);
};

// TSS color coding
const getTssColor = (tss: number): string => {
  if (tss === 0) return "text-zinc-600";
  if (tss < 50) return "text-green-400";
  if (tss < 100) return "text-yellow-400";
  return "text-red-400";
};

// Get modality icon
const getModalityIcon = (modality: string | null) => {
  switch (modality) {
    case "Running":
      return Activity;
    case "Cycling":
      return Bike;
    case "Swimming":
      return Waves;
    case "Strength":
    case "Hypertrophy":
      return Dumbbell;
    case "Conditioning":
      return Timer;
    default:
      return Activity;
  }
};

// Get difficulty rating from TSS
const getDifficultyRating = (tss: number): { label: string; color: string } => {
  if (tss < 50) return { label: "Easy", color: "text-green-400" };
  if (tss < 100) return { label: "Moderate", color: "text-yellow-400" };
  if (tss < 150) return { label: "Hard", color: "text-orange-400" };
  return { label: "Extreme", color: "text-red-400" };
};

// Get duration from structure
const getDuration = (structure: WorkoutBlock[] | null): number => {
  if (!structure) return 0;
  return structure.reduce((total: number, block: WorkoutBlock) => {
    const blockDuration = block.steps.reduce(
      (blockTotal: number, step: WorkoutBlock["steps"][0]) =>
        blockTotal + step.duration_mins,
      0,
    );
    return total + blockDuration * block.repeat_count;
  }, 0);
};

// Get main movements from structure
const getMainMovements = (structure: WorkoutBlock[] | null): string[] => {
  if (!structure) return [];
  const movements: string[] = [];
  for (const block of structure) {
    for (const step of block.steps) {
      if (movements.length < 3 && !movements.includes(step.name)) {
        movements.push(step.name);
      }
    }
  }
  return movements;
};

function DayCard({
  day,
  onToggleLock,
  onClick,
  onEdit,
  onRestDay,
  onDelete,
}: DayCardProps): ReactElement {
  const hasWorkout = !!day.workout_id;
  const restDay = isRestDay(day);

  const handleLockClick = (e: React.MouseEvent<HTMLButtonElement>): void => {
    e.stopPropagation();
    onToggleLock(day.day_index);
  };

  const handleEditClick = (e: React.MouseEvent<HTMLButtonElement>): void => {
    e.stopPropagation();
    onEdit(day.day_index);
  };

  const handleDeleteClick = (e: React.MouseEvent<HTMLButtonElement>): void => {
    e.stopPropagation();
    if (onDelete && window.confirm("Delete this workout?")) {
      onDelete(day.day_index);
    }
  };

  const handleRestDayClick = (e: React.MouseEvent<HTMLButtonElement>): void => {
    e.stopPropagation();
    if (onRestDay) {
      onRestDay(day.day_index);
    }
  };

  // Rest day styling
  if (restDay) {
    return (
      <div className="relative min-h-[180px] p-5 rounded-2xl border border-zinc-800/50 bg-zinc-900/30 transition-all duration-500 group hover:border-zinc-700">
        {/* Day Header */}
        <div className="flex justify-between items-center mb-6">
          <span className="text-[10px] font-black text-zinc-500 tracking-[0.2em] uppercase">
            Day {day.day_index + 1}
          </span>
          <button
            onClick={handleLockClick}
            className="transition-colors hover:text-blue-400 relative z-10"
          >
            {day.is_user_locked ? (
              <Lock className="w-4 h-4 text-blue-400" />
            ) : (
              <Unlock className="w-4 h-4 text-zinc-700 group-hover:text-zinc-500" />
            )}
          </button>
        </div>

        {/* Rest Day Content */}
        <div className="flex flex-col items-center justify-center h-24">
          <BatteryCharging className="w-8 h-8 text-blue-400/50 mb-2" />
          <span className="text-xs font-bold text-blue-400/70 uppercase tracking-widest">
            Rest Day
          </span>
          <span className="text-[10px] text-zinc-600 mt-1">
            Recovery is training
          </span>
        </div>
      </div>
    );
  }

  // Empty day - show add workout and rest day buttons
  if (!hasWorkout) {
    return (
      <div className="relative min-h-[180px] p-5 rounded-2xl border border-dashed border-zinc-800 transition-all duration-500 group hover:border-zinc-700 hover:bg-zinc-900/20">
        {/* Day Header */}
        <div className="flex justify-between items-center mb-6">
          <span className="text-[10px] font-black text-zinc-600 tracking-[0.2em] uppercase">
            Day {day.day_index + 1}
          </span>
          <button
            onClick={handleLockClick}
            className="transition-colors hover:text-hybrid-neon relative z-10"
          >
            {day.is_user_locked ? (
              <Lock className="w-4 h-4 text-hybrid-neon" />
            ) : (
              <Unlock className="w-4 h-4 text-zinc-800 group-hover:text-zinc-600" />
            )}
          </button>
        </div>

        {/* Split Action Buttons */}
        <div className="flex gap-2 h-24">
          {/* Add Workout - 2/3 */}
          <button
            onClick={handleEditClick}
            className="flex-[2] flex flex-col items-center justify-center gap-2 text-zinc-700 hover:text-hybrid-neon hover:border-hybrid-neon/30 hover:bg-zinc-800/30 border border-transparent rounded-xl transition-all"
          >
            <Plus className="w-5 h-5" />
            <span className="text-[9px] font-bold uppercase tracking-wider">
              Add Workout
            </span>
          </button>

          {/* Rest Day - 1/3 */}
          <button
            onClick={handleRestDayClick}
            className="flex-1 flex flex-col items-center justify-center gap-1 text-zinc-600 hover:text-blue-400 hover:border-blue-400/30 hover:bg-blue-400/5 border border-transparent rounded-xl transition-all"
          >
            <BatteryCharging className="w-4 h-4" />
            <span className="text-[9px] font-bold uppercase tracking-wider">
              Rest
            </span>
          </button>
        </div>
      </div>
    );
  }

  // Workout day - normal styling with edit capability
  const ModalityIcon = getModalityIcon(day.modality);
  const difficulty = getDifficultyRating(day.tss);
  const duration = getDuration(day.structure);
  const mainMovements = getMainMovements(day.structure);
  const blockCount = day.structure?.length || 0;
  const stepCount =
    day.structure?.reduce((total, block) => total + block.steps.length, 0) || 0;

  return (
    <div
      onClick={onClick}
      className="relative min-h-[220px] p-5 rounded-2xl border transition-all duration-500 group bg-zinc-900 border-zinc-700 shadow-xl cursor-pointer hover:border-hybrid-neon/50"
    >
      {/* Day Header */}
      <div className="flex justify-between items-center mb-4">
        <span className="text-[10px] font-black text-zinc-600 tracking-[0.2em] uppercase">
          Day {day.day_index + 1}
        </span>
        <div className="flex items-center gap-1">
          <button
            onClick={handleEditClick}
            className="p-1 transition-colors hover:text-hybrid-neon text-zinc-700"
            title="Edit workout"
          >
            <Edit3 className="w-3.5 h-3.5" />
          </button>
          {onDelete && (
            <button
              onClick={handleDeleteClick}
              className="p-1 transition-colors hover:text-red-500 text-zinc-700"
              title="Delete workout"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
          <button
            onClick={handleLockClick}
            className="p-1 transition-colors hover:text-hybrid-neon relative z-10"
          >
            {day.is_user_locked ? (
              <Lock className="w-4 h-4 text-hybrid-neon" />
            ) : (
              <Unlock className="w-4 h-4 text-zinc-800 group-hover:text-zinc-600" />
            )}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
        {/* Title with icon */}
        <div className="flex items-start gap-2 mb-3">
          <ModalityIcon className="w-4 h-4 text-hybrid-neon mt-0.5 flex-shrink-0" />
          <h3 className="font-bold text-sm leading-tight text-white group-hover:text-hybrid-neon transition-colors line-clamp-2">
            {day.title}
          </h3>
        </div>

        {/* Modality and Focus badges */}
        <div className="flex items-center gap-2 mb-3">
          <span className="text-[8px] font-black bg-zinc-800 text-zinc-400 px-2 py-0.5 rounded tracking-widest uppercase">
            {day.modality}
          </span>
          {day.focus && (
            <span className="text-[8px] font-black bg-zinc-800/50 text-zinc-500 px-2 py-0.5 rounded tracking-widest uppercase">
              {day.focus}
            </span>
          )}
        </div>

        {/* Main movements */}
        {mainMovements.length > 0 && (
          <div className="mb-3">
            <div className="flex flex-wrap gap-1">
              {mainMovements.map((movement, idx) => (
                <span
                  key={idx}
                  className="text-[8px] text-zinc-500 bg-zinc-800/30 px-1.5 py-0.5 rounded"
                >
                  {movement}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Metrics row */}
        <div className="flex items-center gap-3 text-[8px]">
          <div className={`flex items-center gap-1 ${getTssColor(day.tss)}`}>
            <Zap className="w-3 h-3 fill-current" />
            <span className="text-[9px] font-black tracking-wider">
              {Math.round(day.tss)} TSS
            </span>
          </div>
          <div className="flex items-center gap-1 text-zinc-500">
            <Timer className="w-3 h-3" />
            <span className="font-black tracking-wider">{duration}m</span>
          </div>
          <div className={`flex items-center gap-1 ${difficulty.color}`}>
            <span className="font-black tracking-wider">
              {difficulty.label}
            </span>
          </div>
        </div>

        {/* Structure preview */}
        {blockCount > 0 && (
          <div className="mt-2 text-[8px] text-zinc-600 font-black tracking-wider">
            {blockCount} block{blockCount !== 1 ? "s" : ""} • {stepCount} step
            {stepCount !== 1 ? "s" : ""}
          </div>
        )}
      </div>
    </div>
  );
}

export default DayCard;
