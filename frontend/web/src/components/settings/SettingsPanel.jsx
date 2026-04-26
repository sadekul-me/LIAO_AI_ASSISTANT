import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";
import {
  Volume2, Moon, Mic, Cpu, Trash2, Shield, Sparkles, 
  Settings as SettingsIcon, ChevronRight, Zap, Database, 
  Fingerprint, Activity, Terminal, Brain, Star, Code, Briefcase,
  Layers, Gauge, MessageSquare, Globe
} from "lucide-react";

export default function SettingsPanel({ isOpen, onClearChat }) {
  const [settings, setSettings] = useState({
    voice: true,
    darkMode: true,
    autoListen: false,
    provider: "gemini",
    personality: "nilima",
    animations: true,
    secureMode: true,
    verbosity: 75,
    contextDepth: "High",
    temperature: "Balanced",
    language: "Bilingual",
    autoTranslate: false
  });

  useEffect(() => {
    const saved = localStorage.getItem("liao_settings");
    if (saved) {
      try { setSettings(JSON.parse(saved)); } catch {}
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("liao_settings", JSON.stringify(settings));
    document.documentElement.classList.toggle("dark", settings.darkMode);
  }, [settings]);

  const update = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  const moods = [
    { id: "nilima", name: "Nilima Core", icon: Star, desc: "Emotional & Intuitive" },
    { id: "developer", name: "Dev Mode", icon: Code, desc: "Technical & Precise" },
    { id: "formal", name: "Formal", icon: Briefcase, desc: "Polished & Business" }
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 z-40 flex flex-col bg-[#050914] overflow-hidden"
        >
          {/* 🌌 DYNAMIC BACKGROUND */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.03]" />
            <div className="absolute top-[-10%] left-[20%] w-[60%] h-[40%] bg-cyan-500/5 blur-[120px] rounded-full" />
          </div>

          {/* 🛰️ HEADER */}
          <header className="shrink-0 p-8 lg:px-12 border-b border-white/[0.05] bg-white/[0.01] backdrop-blur-xl relative z-20">
            <div className="max-w-[1600px] mx-auto flex items-center justify-between">
              <div className="flex items-center gap-6">
                <div className="relative p-4 bg-[#0A0C16] border border-cyan-400/30 rounded-2xl">
                  <SettingsIcon size={24} className="text-cyan-400 animate-[spin_20s_linear_infinite]" />
                </div>
                <div>
                  <h2 className="text-xl font-black uppercase tracking-[8px] text-white">System Core</h2>
                  <p className="text-[10px] font-mono text-cyan-400/40 uppercase tracking-[0.4em] mt-1">Lì Ào Protocol v3.0.2 // Root Access</p>
                </div>
              </div>
            </div>
          </header>

          {/* 🎛️ BALANCED GRID CONTENT */}
          <div className="flex-1 p-8 lg:p-12 overflow-hidden relative z-20">
            <div className="max-w-[1600px] mx-auto h-full flex flex-col">
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 flex-1">
                
                {/* COLUMN 1: INTELLECT */}
                <div className="space-y-10">
                  <Section title="Personality Matrix" icon={Brain}>
                    <div className="flex flex-col gap-4">
                      {moods.map((mood) => {
                        const isActive = settings.personality === mood.id;
                        return (
                          <button
                            key={mood.id}
                            onClick={() => update("personality", mood.id)}
                            className={`p-5 rounded-2xl border transition-all duration-500 text-left ${
                              isActive ? 'border-cyan-400 bg-cyan-400/10 shadow-[0_0_20px_rgba(34,211,238,0.1)]' : 'border-white/5 bg-white/[0.02] hover:bg-white/[0.05]'
                            }`}
                          >
                            <div className="flex items-center gap-4">
                              <mood.icon size={20} className={isActive ? 'text-cyan-400' : 'text-slate-500'} />
                              <div>
                                <h4 className={`text-xs font-bold uppercase tracking-widest ${isActive ? 'text-white' : 'text-slate-400'}`}>{mood.name}</h4>
                                <p className="text-[10px] text-slate-600 mt-1 uppercase">{mood.desc}</p>
                              </div>
                            </div>
                          </button>
                        )
                      })}
                    </div>
                  </Section>

                  <Section title="Cognitive Parameters" icon={Gauge}>
                    <div className="space-y-6">
                      <Dropdown label="Context Depth" value={settings.contextDepth} options={["Low", "Medium", "High"]} onSelect={(v) => update("contextDepth", v)} />
                      <Dropdown label="Temperature" value={settings.temperature} options={["Logical", "Balanced", "Creative"]} onSelect={(v) => update("temperature", v)} />
                    </div>
                  </Section>
                </div>

                {/* COLUMN 2: INTERFACE & LANGUAGE */}
                <div className="space-y-10">
                  <Section title="Linguistic Core" icon={Globe}>
                    <div className="grid grid-cols-3 gap-3">
                      {["English", "Bengali", "Bilingual"].map((lang) => (
                        <button
                          key={lang}
                          onClick={() => update("language", lang)}
                          className={`py-4 text-[9px] font-black uppercase border rounded-xl transition-all ${
                            settings.language === lang ? "bg-cyan-400 text-black border-cyan-400" : "bg-white/[0.02] border-white/5 text-slate-500 hover:text-slate-300"
                          }`}
                        >
                          {lang}
                        </button>
                      ))}
                    </div>
                    <Toggle icon={Sparkles} label="Auto-Translate" desc="Real-time response translation" value={settings.autoTranslate} onChange={(v) => update("autoTranslate", v)} />
                  </Section>

                  <Section title="Neural Interface" icon={Activity}>
                    <div className="space-y-4">
                      <Toggle icon={Volume2} label="Audio Synthesis" desc="AI Vocalization engine" value={settings.voice} onChange={(v) => update("voice", v)} />
                      <Toggle icon={Mic} label="Active Listening" desc="Hands-free voice trigger" value={settings.autoListen} onChange={(v) => update("autoListen", v)} />
                    </div>
                  </Section>
                </div>

                {/* COLUMN 3: SYSTEM & ENGINE */}
                <div className="space-y-10">
                  <Section title="Global Logic" icon={Zap}>
                    <div className="p-6 bg-white/[0.02] border border-white/5 rounded-3xl space-y-6">
                      <div className="flex justify-between items-center text-[10px] font-mono text-slate-500 uppercase">
                        <span>Concise</span>
                        <span className="text-cyan-400">{settings.verbosity}% Elaborate</span>
                        <span>Detailed</span>
                      </div>
                      <input 
                        type="range" min="0" max="100" value={settings.verbosity} 
                        onChange={(e) => update("verbosity", e.target.value)}
                        className="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-cyan-400"
                      />
                    </div>
                    <Toggle icon={Moon} label="Stealth Mode" desc="OLED Optimized interface" value={settings.darkMode} onChange={(v) => update("darkMode", v)} />
                  </Section>

                  <Section title="Memory & Storage" icon={Database}>
                    <div className="space-y-4">
                      <div className="p-5 border border-cyan-400/20 bg-cyan-400/5 rounded-2xl flex items-center justify-between">
                         <div className="flex items-center gap-3">
                            <Cpu size={18} className="text-cyan-400" />
                            <span className="text-[10px] font-black uppercase text-slate-300">Engine: {settings.provider}</span>
                         </div>
                         <div className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
                      </div>
                      <button
                        onClick={onClearChat}
                        className="w-full group flex items-center justify-between p-5 bg-red-500/5 border border-red-500/10 hover:border-red-500/40 rounded-2xl transition-all"
                      >
                        <div className="flex items-center gap-4">
                          <Trash2 size={18} className="text-red-500" />
                          <span className="text-[10px] font-bold uppercase text-red-500 tracking-wider">Purge Chat History</span>
                        </div>
                        <ChevronRight size={16} className="text-red-900" />
                      </button>
                    </div>
                  </Section>
                </div>

              </div>

              {/* 🛰️ FOOTER STATUS BAR */}
              <div className="mt-auto pt-8 border-t border-white/[0.05] flex items-center justify-between opacity-40">
                <div className="flex gap-8 text-[9px] font-mono uppercase tracking-[0.2em] text-slate-500">
                  <span>Hardware ID: SADIK_ENG_2026</span>
                  <span>Latency: 12ms</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-1 w-12 bg-cyan-500/20 rounded-full overflow-hidden">
                    <motion.div animate={{ x: [-48, 48] }} transition={{ repeat: Infinity, duration: 2 }} className="h-full w-6 bg-cyan-400" />
                  </div>
                  <span className="text-[9px] font-mono uppercase text-cyan-400">System Stable</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// --- Specialized UI Components ---
function Section({ title, icon: Icon, children }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Icon size={18} className="text-cyan-400 opacity-60" />
        <h3 className="text-[11px] font-black uppercase tracking-[0.4em] text-slate-500">{title}</h3>
        <div className="h-px flex-1 bg-gradient-to-r from-white/5 to-transparent" />
      </div>
      <div className="space-y-4">{children}</div>
    </div>
  );
}

function Toggle({ icon: Icon, label, desc, value, onChange }) {
  return (
    <div onClick={() => onChange(!value)} className="group flex items-center justify-between p-4 bg-white/[0.01] border border-white/[0.05] hover:border-cyan-400/30 rounded-2xl transition-all cursor-pointer">
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-xl transition-all ${value ? 'bg-cyan-400 text-black shadow-[0_0_15px_rgba(34,211,238,0.4)]' : 'bg-white/5 text-slate-600'}`}>
          <Icon size={18} />
        </div>
        <div>
          <p className="text-[10px] font-bold text-slate-200 uppercase tracking-wide">{label}</p>
          <p className="text-[8px] text-slate-600 mt-1 uppercase">{desc}</p>
        </div>
      </div>
      <div className={`w-10 h-4 rounded-full relative transition-colors ${value ? 'bg-cyan-400/40' : 'bg-slate-800'}`}>
        <motion.div animate={{ x: value ? 24 : 4 }} className="absolute top-1 h-2 w-2 rounded-full bg-white shadow-[0_0_8px_white]" />
      </div>
    </div>
  );
}

function Dropdown({ label, value, options, onSelect }) {
  return (
    <div className="space-y-2">
      <label className="text-[9px] font-bold text-slate-600 uppercase tracking-widest ml-1">{label}</label>
      <div className="relative group">
        <select 
          value={value} onChange={(e) => onSelect(e.target.value)}
          className="w-full bg-white/[0.02] border border-white/5 text-slate-300 text-[10px] font-bold uppercase p-4 rounded-2xl appearance-none outline-none focus:border-cyan-400/50 transition-all cursor-pointer"
        >
          {options.map(opt => <option key={opt} value={opt} className="bg-[#050914]">{opt}</option>)}
        </select>
        <ChevronRight size={14} className="absolute right-4 top-1/2 -translate-y-1/2 rotate-90 text-slate-600 pointer-events-none" />
      </div>
    </div>
  );
}