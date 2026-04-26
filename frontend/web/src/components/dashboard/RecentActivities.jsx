import GlassCard from "../ui/GlassCard";
import { CheckCircle, AlertCircle, Clock } from "lucide-react";

const activities = [
  {
    id: 1,
    title: "Calculator app created",
    time: "Just now",
    icon: CheckCircle,
    color: "text-blue-400",
    bg: "bg-blue-500/10",
  },
  {
    id: 2,
    title: "VS Code opened",
    time: "2 min ago",
    icon: CheckCircle,
    color: "text-indigo-400",
    bg: "bg-indigo-500/10",
  },
  {
    id: 3,
    title: "System optimized",
    time: "10 min ago",
    icon: AlertCircle,
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
  },
  {
    id: 4,
    title: "Files cleaned",
    time: "15 min ago",
    icon: Clock,
    color: "text-amber-400",
    bg: "bg-amber-500/10",
  },
];

const RecentActivities = () => {
  return (
    <GlassCard
      className="
        h-full
        p-4
        rounded-3xl
        bg-gradient-to-br from-[#0b1220] to-[#020617]
        flex flex-col
      "
    >
      {/* 🔹 Header */}
      <div className="flex items-center justify-between mb-3 flex-shrink-0">
        <h2 className="text-sm font-semibold text-slate-300">
          Recent Activities
        </h2>

        <button className="text-[11px] text-blue-400 hover:text-blue-300 transition">
          View All
        </button>
      </div>

      {/* 🔹 List */}
      <div className="flex-1 flex flex-col justify-between min-h-0">
        {activities.map((item, i) => {
          const Icon = item.icon;

          return (
            <div
              key={item.id}
              className={`
                flex items-center justify-between
                py-2
                min-h-[42px]
                ${i !== activities.length - 1 ? "border-b border-white/5" : ""}
              `}
            >
              {/* Left */}
              <div className="flex items-center gap-2.5 min-w-0">
                {/* Icon */}
                <div
                  className={`
                    w-7 h-7
                    rounded-lg
                    flex items-center justify-center
                    flex-shrink-0
                    ${item.bg}
                  `}
                >
                  <Icon size={14} className={item.color} />
                </div>

                {/* Text */}
                <span className="text-[13px] text-slate-300 truncate">
                  {item.title}
                </span>
              </div>

              {/* Time */}
              <span className="text-[11px] text-slate-500 flex-shrink-0 ml-2">
                {item.time}
              </span>
            </div>
          );
        })}
      </div>
    </GlassCard>
  );
};

export default RecentActivities;