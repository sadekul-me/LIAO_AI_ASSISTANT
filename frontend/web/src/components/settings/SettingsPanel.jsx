import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Volume2,
  Mic,
  Shield,
  Sparkles,
  Settings as SettingsIcon,
  ChevronRight,
  Database,
  Activity,
  Brain,
  Star,
  Code,
  Briefcase,
  Gauge,
  Globe,
  Command,
  Sliders,
} from "lucide-react";

export default function SettingsPanel({ onClearChat }) {
  const [settings, setSettings] = useState({
    voice: true,
    darkMode: true,
    autoListen: false,
    autoTranslate: true,
    provider: "Gemini 1.5 Pro",
    personality: "nilima",
    secureMode: true,
    verbosity: 75,
    contextDepth: "High",
    temperature: "Balanced",
    language: "Bilingual",
  });

  useEffect(() => {
    const saved = localStorage.getItem("liao_settings");
    if (saved) {
      try {
        setSettings(JSON.parse(saved));
      } catch {}
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("liao_settings", JSON.stringify(settings));
    document.documentElement.classList.toggle("dark", settings.darkMode);
  }, [settings]);

  const update = (key, value) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <div className="relative h-full w-full flex items-center justify-center overflow-hidden bg-transparent p-4 lg:p-6">
      {/* Ambient Background Effects */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute top-[-120px] right-[-80px] h-96 w-96 rounded-full bg-cyan-500/5 blur-[150px]" />
        <div className="absolute bottom-[-120px] left-[-100px] h-96 w-96 rounded-full bg-blue-500/5 blur-[150px]" />
      </div>

      {/* Main Panel Content */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative flex h-full max-h-[850px] w-full max-w-7xl flex-col overflow-hidden rounded-[34px] border border-white/10 bg-[#050810]/60 backdrop-blur-3xl shadow-2xl"
      >
        {/* Decorative Grid Accents */}
        <div className="absolute left-1/3 top-0 h-full w-px bg-gradient-to-b from-transparent via-cyan-500/10 to-transparent" />
        <div className="absolute right-1/3 top-0 h-full w-px bg-gradient-to-b from-transparent via-white/5 to-transparent" />

        {/* Header */}
        <header className="relative z-10 flex shrink-0 items-center justify-between border-b border-white/5 bg-white/[0.02] px-8 py-6">
          <div className="flex items-center gap-5">
            <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-4 shadow-[0_0_20px_rgba(6,182,212,0.15)]">
              <SettingsIcon
                size={22}
                className="text-cyan-400 animate-[spin_12s_linear_infinite]"
              />
            </div>
            <div>
              <h2 className="text-sm font-black uppercase tracking-[0.42em] text-white">
                System Configuration
              </h2>
              <div className="mt-1 flex items-center gap-3 text-[10px] font-mono uppercase tracking-widest text-cyan-400/60">
                <span>Node: SADIK_ENG</span>
                <span className="h-1 w-1 rounded-full bg-slate-700" />
                <span>Protocol: v3.0.2</span>
              </div>
            </div>
          </div>
        </header>

        {/* Settings Body - Scrollable only if needed */}
        <div className="relative z-10 flex-1 overflow-y-auto no-scrollbar px-8 py-8">
          <div className="grid grid-cols-1 gap-10 xl:grid-cols-12">
            
            {/* LEFT COLUMN: AI Personality */}
            <div className="xl:col-span-4 space-y-10">
              <Section title="Personality Matrix" icon={Brain}>
                <div className="space-y-3">
                  <PersonalityCard
                    active={settings.personality === "nilima"}
                    onClick={() => update("personality", "nilima")}
                    icon={Star}
                    title="Nilima Core"
                    desc="Emotional & Intuitive"
                    color="text-pink-400"
                  />
                  <PersonalityCard
                    active={settings.personality === "developer"}
                    onClick={() => update("personality", "developer")}
                    icon={Code}
                    title="Dev Mode"
                    desc="Logic & Technical"
                    color="text-cyan-400"
                  />
                  <PersonalityCard
                    active={settings.personality === "formal"}
                    onClick={() => update("personality", "formal")}
                    icon={Briefcase}
                    title="Corporate"
                    desc="Polished & Precise"
                    color="text-blue-400"
                  />
                </div>
              </Section>

              <Section title="Cognitive Parameters" icon={Gauge}>
                <div className="space-y-4">
                  <Dropdown
                    label="Context Depth"
                    value={settings.contextDepth}
                    options={["Standard", "Balanced", "High"]}
                    onSelect={(v) => update("contextDepth", v)}
                  />
                  <Dropdown
                    label="Temperature"
                    value={settings.temperature}
                    options={["Logical", "Balanced", "Creative"]}
                    onSelect={(v) => update("temperature", v)}
                  />
                </div>
              </Section>
            </div>

            {/* MIDDLE COLUMN: Interface Controls */}
            <div className="xl:col-span-4 space-y-10 xl:border-x xl:border-white/5 xl:px-8">
              <Section title="Neural Interface" icon={Activity}>
                <div className="space-y-3">
                  <Toggle
                    icon={Volume2}
                    label="Audio Synthesis"
                    desc="AI Vocal Engine"
                    value={settings.voice}
                    onChange={(v) => update("voice", v)}
                    color="cyan"
                  />
                  <Toggle
                    icon={Mic}
                    label="Active Listening"
                    desc="Wake Trigger"
                    value={settings.autoListen}
                    onChange={(v) => update("autoListen", v)}
                    color="purple"
                  />
                  <Toggle
                    icon={Sparkles}
                    label="Auto Translate"
                    desc="Realtime Engine"
                    value={settings.autoTranslate}
                    onChange={(v) => update("autoTranslate", v)}
                    color="emerald"
                  />
                </div>
              </Section>

              <Section title="Linguistic Hub" icon={Globe}>
                <div className="flex rounded-2xl border border-white/5 bg-white/[0.02] p-1.5">
                  {["English", "Bengali", "Bilingual"].map((lang) => (
                    <button
                      key={lang}
                      onClick={() => update("language", lang)}
                      className={`flex-1 rounded-xl py-3 text-[10px] font-black uppercase transition-all ${
                        settings.language === lang
                          ? "bg-cyan-500 text-black shadow-lg shadow-cyan-500/20"
                          : "text-slate-500 hover:text-slate-300"
                      }`}
                    >
                      {lang}
                    </button>
                  ))}
                </div>
              </Section>
            </div>

            {/* RIGHT COLUMN: Performance & Security */}
            <div className="xl:col-span-4 space-y-10">
              <Section title="Output Tuning" icon={Sliders}>
                <div className="rounded-[26px] border border-white/5 bg-white/[0.02] p-6 space-y-5">
                  <div className="flex items-center justify-between text-[10px] font-mono uppercase">
                    <span className="text-slate-600">Concise</span>
                    <span className="font-black text-cyan-400">{settings.verbosity}% Elaborate</span>
                    <span className="text-slate-600">Deep</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={settings.verbosity}
                    onChange={(e) => update("verbosity", e.target.value)}
                    className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                  />
                </div>
              </Section>

              <Section title="Security & Data" icon={Shield}>
                <div className="space-y-4">
                  <div className="flex items-center justify-between rounded-2xl border border-white/5 bg-white/[0.03] p-5">
                    <div className="flex items-center gap-4">
                      <div className="rounded-xl bg-emerald-500/10 p-2.5 text-emerald-400">
                        <Database size={18} />
                      </div>
                      <div>
                        <p className="text-[10px] font-black uppercase text-slate-200">Provider Status</p>
                        <p className="text-[9px] font-mono uppercase text-slate-600">
                          {settings.provider} // Active
                        </p>
                      </div>
                    </div>
                    <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                  </div>

                  <button
                    onClick={onClearChat}
                    className="flex w-full items-center justify-between rounded-2xl border border-red-500/10 bg-red-500/[0.03] p-6 transition-all hover:bg-red-500/[0.06] hover:border-red-500/30 group"
                  >
                    <span className="text-[10px] font-black uppercase tracking-[0.18em] text-red-400 group-hover:text-red-500">
                      Purge Neural Memory
                    </span>
                    <ChevronRight size={14} className="text-red-900 group-hover:text-red-500 transition-colors" />
                  </button>
                </div>
              </Section>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="relative z-10 flex shrink-0 items-center justify-between border-t border-white/5 bg-white/[0.02] px-8 py-5 opacity-60">
          <div className="flex gap-8 text-[9px] font-mono uppercase tracking-[0.2em] text-slate-500">
            <span>Node ID: {navigator.platform}</span>
            <span>Status: Operational</span>
          </div>
          <div className="flex items-center gap-2.5 text-cyan-500">
            <Command size={14} />
            <span className="text-[9px] font-black uppercase tracking-widest">
              Lì Ào Protocol Synchronized
            </span>
          </div>
        </footer>
      </motion.div>
    </div>
  );
}

// --- Helper Components ---

function Section({ title, icon: Icon, children }) {
  return (
    <div className="space-y-5">
      <div className="flex items-center gap-3 ml-1">
        <Icon size={16} className="text-cyan-400" />
        <h3 className="text-[11px] font-black uppercase tracking-[0.26em] text-slate-500">
          {title}
        </h3>
      </div>
      {children}
    </div>
  );
}

function PersonalityCard({ active, onClick, icon: Icon, title, desc, color }) {
  return (
    <button
      onClick={onClick}
      className={`relative flex w-full items-center gap-5 overflow-hidden rounded-[26px] border p-5 text-left transition-all ${
        active
          ? "border-cyan-500/30 bg-white/[0.06] shadow-xl shadow-black/20"
          : "border-white/5 bg-transparent hover:border-white/10 hover:bg-white/[0.02]"
      }`}
    >
      <div className={`rounded-2xl p-3.5 transition-colors ${active ? `bg-white/10 ${color}` : "bg-white/5 text-slate-700"}`}>
        <Icon size={20} />
      </div>
      <div className="flex-1">
        <p className={`text-[11px] font-black uppercase tracking-wider ${active ? "text-white" : "text-slate-500"}`}>
          {title}
        </p>
        <p className="mt-1 text-[9px] uppercase text-slate-600 font-medium">
          {desc}
        </p>
      </div>
      {active && <div className="absolute right-0 top-1/4 h-1/2 w-1 rounded-l-full bg-cyan-500" />}
    </button>
  );
}

function Toggle({ icon: Icon, label, desc, value, onChange, color }) {
  const colorMap = {
    cyan: "text-cyan-400 bg-cyan-400/10",
    purple: "text-purple-400 bg-purple-400/10",
    emerald: "text-emerald-400 bg-emerald-400/10",
  };

  return (
    <button
      onClick={() => onChange(!value)}
      className="flex w-full items-center justify-between rounded-[22px] border border-white/5 bg-white/[0.02] p-5 transition-all hover:border-white/10"
    >
      <div className="flex items-center gap-4">
        <div className={`rounded-xl p-3 transition-all ${value ? colorMap[color] : "bg-white/5 text-slate-800"}`}>
          <Icon size={18} />
        </div>
        <div className="text-left">
          <p className="text-[10px] font-bold uppercase tracking-tight text-slate-200">{label}</p>
          <p className="text-[8px] uppercase text-slate-600 mt-0.5">{desc}</p>
        </div>
      </div>
      <div className={`relative h-5 w-11 rounded-full transition-colors ${value ? "bg-cyan-500" : "bg-white/10"}`}>
        <motion.div
          animate={{ x: value ? 24 : 4 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
          className="absolute top-1 h-3 w-3 rounded-full bg-white shadow-sm"
        />
      </div>
    </button>
  );
}

function Dropdown({ label, value, options, onSelect }) {
  return (
    <div className="space-y-2.5">
      <label className="ml-2 text-[9px] font-black uppercase tracking-[0.2em] text-slate-600">
        {label}
      </label>
      <div className="relative group">
        <select
          value={value}
          onChange={(e) => onSelect(e.target.value)}
          className="w-full appearance-none rounded-2xl border border-white/5 bg-white/[0.03] p-4.5 pl-5 text-[10px] font-black uppercase text-slate-300 outline-none focus:border-cyan-500/40 transition-all cursor-pointer"
        >
          {options.map((opt) => (
            <option key={opt} value={opt} className="bg-[#0b0f1a] text-white">{opt}</option>
          ))}
        </select>
        <ChevronRight size={14} className="pointer-events-none absolute right-5 top-1/2 -translate-y-1/2 rotate-90 text-slate-600 group-hover:text-cyan-500 transition-colors" />
      </div>
    </div>
  );
}