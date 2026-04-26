// components/dashboard/QuickActions.jsx

import GlassCard from "../ui/GlassCard";
import {
  Code2,
  Sparkles,
  Trash2,
  Mic,
  Camera,
  Power,
} from "lucide-react";

const actions = [
  {
    id: "vscode",
    label: "Open VS Code",
    icon: Code2,
    color: "from-blue-500 to-cyan-400",
  },
  {
    id: "optimize",
    label: "Optimize System",
    icon: Sparkles,
    color: "from-purple-500 to-indigo-500",
  },
  {
    id: "clear",
    label: "Clear Temp Files",
    icon: Trash2,
    color: "from-cyan-500 to-blue-500",
  },
  {
    id: "voice",
    label: "Voice Command",
    icon: Mic,
    color: "from-indigo-500 to-purple-500",
  },
  {
    id: "screenshot",
    label: "Take Screenshot",
    icon: Camera,
    color: "from-pink-500 to-rose-500",
  },
  {
    id: "shutdown",
    label: "Shutdown PC",
    icon: Power,
    color: "from-red-500 to-orange-500",
  },
];

const QuickActions = () => {
  return (
    <GlassCard className="p-4 rounded-3xl bg-gradient-to-br from-[#0b1220] to-[#020617]">
      
      {/* 🔹 Header */}
      <h2 className="text-sm font-semibold text-slate-300 mb-3">
        Quick Actions
      </h2>

      {/* 🔹 Grid */}
      <div className="grid grid-cols-3 gap-2.5">
        {actions.map((action) => {
          const Icon = action.icon;

          return (
            <button
              key={action.id}
              className="
                group
                flex flex-col items-center justify-center
                gap-1.5
                py-2.5
                rounded-xl
                bg-white/[0.03]
                border border-white/5
                hover:bg-white/[0.06]
                transition-all duration-300
              "
            >
              {/* 🔹 Icon Box */}
              <div
                className={`
                  w-8 h-8
                  rounded-lg
                  bg-gradient-to-br ${action.color}
                  flex items-center justify-center
                  shadow-[0_0_12px_rgba(0,0,0,.3)]
                `}
              >
                <Icon size={15} className="text-white" />
              </div>

              {/* 🔹 Label */}
              <span className="text-[10.5px] text-slate-400 text-center leading-tight group-hover:text-white transition">
                {action.label}
              </span>
            </button>
          );
        })}
      </div>
    </GlassCard>
  );
};

export default QuickActions;