import React, { useState, useRef } from "react";
import {
  Home, MessageCircle, Mic, Settings, Code2, Wrench,
  FileText, Cpu, ChevronDown, Shield, Upload, Sparkles
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import clsx from "clsx";

const menu = [
  { id: "dashboard", label: "Dashboard", icon: Home },
  { id: "chat", label: "Chat", icon: MessageCircle },
  { id: "voice", label: "Voice", icon: Mic },
  { id: "automation", label: "Automation", icon: Cpu },
  { id: "code", label: "Code Assistant", icon: Code2 },
  { id: "system", label: "System Control", icon: Shield },
  { id: "files", label: "Files & Search", icon: FileText },
  { id: "tools", label: "Tools", icon: Wrench },
  { id: "settings", label: "Settings", icon: Settings },
];

const Sidebar = () => {
  const [active, setActive] = useState("dashboard");
  const [avatar, setAvatar] = useState(null);
  const [name, setName] = useState("Sadekul Islam");
  const [editName, setEditName] = useState(false);
  const fileRef = useRef(null);

  const handleImage = (e) => {
    const file = e.target.files[0];
    if (file) setAvatar(URL.createObjectURL(file));
  };

  return (
    <aside className="relative flex h-screen w-full flex-col justify-between overflow-hidden border-r border-white/5 bg-gradient-to-b from-[#080E1C] via-[#050914] to-[#03060E] px-4 py-6 md:w-[280px] xl:w-[300px]">
      
      {/* 🔮 Improved Ambient Glows: একটু বেশি ইনটেনসিটি যাতে ডার্কনেস কমে */}
      <div className="pointer-events-none absolute -left-20 top-0 h-64 w-64 rounded-full bg-cyan-600/15 blur-[120px]" />
      <div className="pointer-events-none absolute -right-20 bottom-0 h-64 w-64 rounded-full bg-blue-600/10 blur-[120px]" />

      <div className="relative z-10">
        {/* BRAND LOGO SECTION */}
        <div className="mb-10 flex items-center gap-4 px-2">
          <div className="group relative">
            <div className="absolute inset-0 animate-pulse rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 blur-lg opacity-60 group-hover:opacity-100 transition-opacity" />
            <div className="relative flex h-12 w-12 items-center justify-center rounded-xl border border-white/20 bg-[#0F172A]/80 backdrop-blur-md shadow-2xl">
              <Sparkles className="text-cyan-400 group-hover:rotate-12 transition-transform" size={24} />
            </div>
          </div>
          <div>
            <h2 className="bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-lg font-bold tracking-tight text-transparent">
              Li Ao AI
            </h2>
          </div>
        </div>

        {/* NAVIGATION MENU */}
        <nav className="space-y-1">
          {menu.map((item) => {
            const Icon = item.icon;
            const isActive = active === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setActive(item.id)}
                className={clsx(
                  "group relative flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-300",
                  isActive ? "text-white" : "text-slate-400 hover:bg-white/[0.04] hover:text-slate-200"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 rounded-xl border border-white/10 bg-gradient-to-r from-cyan-500/10 via-transparent to-transparent shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]"
                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                  />
                )}
                <Icon
                  size={19}
                  className={clsx(
                    "relative z-10 transition-all duration-300",
                    isActive ? "text-cyan-400 drop-shadow-[0_0_10px_rgba(34,211,238,0.6)] scale-110" : "group-hover:text-slate-200"
                  )}
                />
                <span className="relative z-10">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* BOTTOM SECTION */}
      <div className="relative z-10 flex flex-col gap-6">
        
        {/* NEON AI CORE (CENTER) */}
        <div className="relative flex flex-col items-center py-4">
          <div className="group relative cursor-pointer">
            <div className="absolute inset-0 animate-[spin_6s_linear_infinite] rounded-full bg-gradient-to-r from-cyan-500 via-blue-500 to-cyan-400 opacity-20 blur-xl group-hover:opacity-50" />
            <div className="relative flex h-20 w-20 items-center justify-center rounded-full border border-white/10 bg-[#0F172A]/60 shadow-2xl backdrop-blur-2xl">
               <div className="h-12 w-12 rounded-full border-2 border-dashed border-cyan-500/30 animate-[spin_10s_linear_infinite] absolute" />
               <span className="bg-gradient-to-br from-cyan-300 to-blue-500 bg-clip-text text-xl font-black text-transparent">AI</span>
            </div>
          </div>
          <p className="mt-4 text-[9px] font-bold tracking-[3px] text-slate-500 uppercase">System Stable</p>
        </div>

        {/* PROFILE CARD */}
        <div className="group relative rounded-2xl border border-white/5 bg-[#1E293B]/20 p-3 transition-all hover:bg-[#1E293B]/40 hover:border-white/10 shadow-lg">
          <input type="file" hidden ref={fileRef} accept="image/*" onChange={handleImage} />
          
          <div className="flex items-center gap-3">
            <div 
              className="relative h-11 w-11 shrink-0 cursor-pointer overflow-hidden rounded-xl border border-white/10 shadow-inner"
              onClick={() => fileRef.current.click()}
            >
              <img src={avatar || "/api/placeholder/48/48"} alt="avatar" className="h-full w-full object-cover" />
              <div className="absolute inset-0 flex items-center justify-center bg-black/60 opacity-0 transition-opacity group-hover:opacity-100">
                <Upload size={14} className="text-white" />
              </div>
            </div>

            <div className="flex flex-1 flex-col min-w-0">
              {editName ? (
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onBlur={() => setEditName(false)}
                  autoFocus
                  className="bg-transparent text-sm font-medium text-white outline-none border-b border-cyan-500/50"
                />
              ) : (
                <div className="flex items-center gap-1">
                  <p onClick={() => setEditName(true)} className="truncate text-sm font-semibold text-slate-200 cursor-text">
                    {name}
                  </p>
                  <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]" />
                </div>
              )}
              <p className="truncate text-[10px] font-medium text-slate-500 uppercase tracking-tight">Li Ao Creator</p>
            </div>
            
            <ChevronDown size={16} className="text-slate-600 group-hover:text-slate-400 transition-colors" />
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;