import { useState, useEffect } from "react";
import { X, Calendar, ChevronDown, Loader2 } from "lucide-react";
import type { PlanSelectorProps } from "@/types";

function PlanSelector({
  isOpen,
  onClose,
  plans,
  currentPlanId,
  onLoadPlan,
  onFetchPlans,
  loading,
}: PlanSelectorProps): React.JSX.Element | null {
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);

  useEffect(() => {
    if (isOpen) {
      onFetchPlans();
    }
  }, [isOpen, onFetchPlans]);

  const handleLoadPlan = (planId: string): void => {
    onLoadPlan(planId);
    setIsDropdownOpen(false);
    onClose();
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  // Mini dropdown version for header
  if (!isOpen && plans.length > 0) {
    return (
      <div className="relative">
        <button
          onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          className="flex items-center gap-2 text-xs font-bold text-zinc-400 hover:text-white transition-colors"
        >
          <Calendar className="w-4 h-4" />
          <span>My Plans</span>
          <ChevronDown
            className={`w-3 h-3 transition-transform ${isDropdownOpen ? "rotate-180" : ""}`}
          />
        </button>

        {isDropdownOpen && (
          <>
            <div
              className="fixed inset-0 z-40"
              onClick={() => setIsDropdownOpen(false)}
            />
            <div className="absolute top-full right-0 mt-2 w-72 bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl z-50 overflow-hidden">
              <div className="p-3 border-b border-zinc-800">
                <span className="text-xs font-bold text-zinc-500 uppercase tracking-wider">
                  Saved Plans
                </span>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {loading ? (
                  <div className="p-4 flex justify-center">
                    <Loader2 className="w-5 h-5 animate-spin text-zinc-500" />
                  </div>
                ) : plans.length === 0 ? (
                  <div className="p-4 text-center text-sm text-zinc-500">
                    No saved plans yet
                  </div>
                ) : (
                  plans.map((plan) => (
                    <button
                      key={plan.id}
                      onClick={() => handleLoadPlan(plan.id)}
                      className={`w-full text-left p-3 hover:bg-zinc-800 transition-colors border-b border-zinc-800/50 last:border-0 ${
                        plan.id === currentPlanId ? "bg-zinc-800/50" : ""
                      }`}
                    >
                      <div className="font-bold text-sm text-white mb-1 truncate">
                        {plan.plan_name}
                      </div>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-zinc-500">
                          {formatDate(plan.created_at)}
                        </span>
                        <span className="text-hybrid-neon">
                          {Math.round(plan.total_tss)} TSS
                        </span>
                      </div>
                    </button>
                  ))
                )}
              </div>
            </div>
          </>
        )}
      </div>
    );
  }

  // Full modal version
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="bg-zinc-900 border border-zinc-800 w-full max-w-lg rounded-3xl overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-zinc-800 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-hybrid-neon/10 rounded-xl flex items-center justify-center">
              <Calendar className="w-5 h-5 text-hybrid-neon" />
            </div>
            <div>
              <h2 className="text-lg font-black text-white uppercase tracking-tighter">
                My Plans
              </h2>
              <p className="text-zinc-500 text-xs">
                {plans.length} saved plan{plans.length !== 1 ? "s" : ""}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-zinc-800 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-zinc-400" />
          </button>
        </div>

        {/* Plan List */}
        <div className="max-h-[60vh] overflow-y-auto">
          {loading ? (
            <div className="p-12 flex justify-center">
              <Loader2 className="w-8 h-8 animate-spin text-zinc-500" />
            </div>
          ) : plans.length === 0 ? (
            <div className="p-12 text-center">
              <Calendar className="w-12 h-12 text-zinc-700 mx-auto mb-4" />
              <p className="text-zinc-500 text-sm">No saved plans yet</p>
              <p className="text-zinc-600 text-xs mt-2">
                Generate and save a plan to see it here
              </p>
            </div>
          ) : (
            <div className="divide-y divide-zinc-800">
              {plans.map((plan) => (
                <div
                  key={plan.id}
                  className={`p-4 hover:bg-zinc-800/50 transition-colors ${
                    plan.id === currentPlanId ? "bg-zinc-800/30" : ""
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-white mb-1 truncate">
                        {plan.plan_name}
                      </h3>
                      <p className="text-xs text-zinc-500 mb-2 line-clamp-2">
                        {plan.user_goal}
                      </p>
                      <div className="flex items-center gap-4 text-xs">
                        <span className="text-zinc-600">
                          {formatDate(plan.created_at)}
                        </span>
                        <span className="text-hybrid-neon font-bold">
                          {Math.round(plan.total_tss)} TSS
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleLoadPlan(plan.id)}
                      className="ml-4 px-4 py-2 bg-zinc-800 hover:bg-hybrid-neon text-white hover:text-black font-bold text-xs rounded-xl transition-all"
                    >
                      Load
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-zinc-800 bg-zinc-900/50">
          <button
            onClick={onClose}
            className="w-full py-3 text-zinc-500 hover:text-white font-bold text-sm transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default PlanSelector;
