import { Cpu, Activity, HardDrive, Zap } from "lucide-react";
import GlassCard from "../ui/GlassCard";

const stats = [
  {
    label: "CPU",
    value: "24%",
    progress: 24,
    color: "from-cyan-400 to-blue-500",
    icon: Cpu,
  },
  {
    label: "RAM",
    value: "61%",
    progress: 61,
    color: "from-indigo-400 to-purple-500",
    icon: Activity,
  },
  {
    label: "Disk",
    value: "43%",
    progress: 43,
    color: "from-yellow-400 to-orange-400",
    icon: HardDrive,
  },
  {
    label: "GPU",
    value: "32%",
    progress: 32,
    color: "from-slate-400 to-slate-500",
    icon: Zap,
  },
];

export default function SystemOverview() {
  return (
    <GlassCard className="p-3 rounded-3xl bg-gradient-to-br from-[#0b1220] to-[#020617]">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-sm text-slate-300 font-semibold">
          System Overview
        </h2>

        <div className="flex items-center gap-1.5 text-[10px] text-emerald-400">
          <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
          Live
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-3">
        {stats.map((item, i) => {
          const Icon = item.icon;

          return (
            <div key={i} className="flex flex-col gap-1">
              {/* Top */}
              <div className="flex items-center gap-1.5">
                <Icon size={12} className="text-slate-400" />

                <span className="text-[10px] text-slate-400">
                  {item.label}
                </span>
              </div>

              {/* Value */}
              <span className="text-[14px] text-white font-semibold">
                {item.value}
              </span>

              {/* Progress */}
              <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r ${item.color}`}
                  style={{ width: `${item.progress}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </GlassCard>
  );
}