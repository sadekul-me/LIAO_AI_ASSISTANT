import { useEffect, useState } from "react";
import { Clock, CalendarDays, Bell, Settings } from "lucide-react";

const SystemBar = () => {
  const [time, setTime] = useState(getTime());
  const [date, setDate] = useState(getDate());

  /* =========================================
     LIVE CLOCK UPDATE
  ========================================= */
  useEffect(() => {
    const interval = setInterval(() => {
      setTime(getTime());
      setDate(getDate());
    }, 1000); // প্রতি 1 sec update

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="
      w-full max-w-[420px] h-12 
      flex items-center justify-between 
      px-[14px] 
      bg-[#0A1220]/65 border border-white/10 
      rounded-[14px] backdrop-blur-[14px] 
      shadow-[0_8px_25px_rgba(0,0,0,0.35)] 
      text-[#DBEAFE] text-[13px]
    ">

      {/* LEFT: TIME */}
      <div className="flex items-center gap-[6px] opacity-90">
        <Clock size={18} />
        <span>{time}</span>
      </div>

      {/* MIDDLE: DATE */}
      <div className="flex-1 flex items-center justify-center gap-[6px] opacity-90">
        <CalendarDays size={18} />
        <span>{date}</span>
      </div>

      {/* RIGHT: ICONS */}
      <div className="flex items-center gap-[10px]">
        <button className="
          w-8 h-8 flex items-center justify-center 
          bg-white/[0.06] border border-white/10 
          rounded-[10px] text-[#CBD5E1] 
          transition-all duration-200 
          hover:bg-white/[0.12] hover:-translate-y-[1px]
        ">
          <Bell size={18} />
        </button>

        <button className="
          w-8 h-8 flex items-center justify-center 
          bg-white/[0.06] border border-white/10 
          rounded-[10px] text-[#CBD5E1] 
          transition-all duration-200 
          hover:bg-white/[0.12] hover:-translate-y-[1px]
        ">
          <Settings size={18} />
        </button>
      </div>

    </div>
  );
};

/* =========================================
   HELPERS
========================================= */
const getTime = () =>
  new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

const getDate = () =>
  new Date().toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "2-digit",
  });

export default SystemBar;