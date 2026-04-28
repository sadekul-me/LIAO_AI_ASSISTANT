import React, { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Terminal,
  Code2,
  Sparkles,
  Wand2,
  Copy,
  Check,
  Play,
  Brackets,
  Cpu,
  Hash,
  Database,
  Globe,
  Download,
  Trash2,
  Zap,
} from "lucide-react";

export default function CodeAssistant() {
  const [prompt, setPrompt] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [activeLang, setActiveLang] = useState("React");

  const languages = [
    { name: "React", icon: Code2, color: "text-cyan-400" },
    { name: "C#", icon: Hash, color: "text-purple-400" },
    { name: "Python", icon: Sparkles, color: "text-blue-400" },
    { name: "SQL", icon: Database, color: "text-amber-400" },
  ];

  const generatedCode = useMemo(() => {
    if (activeLang === "React") {
      return `import React from "react";

export default function Card() {
  return (
    <div className="p-6 rounded-2xl bg-zinc-900 text-white">
      High Performance React UI
    </div>
  );
}`;
    }

    if (activeLang === "C#") {
      return `public class LiaoEngine
{
    public async Task OptimizeCore()
    {
        await System.ConnectAsync("SADIK_NODE");
    }
}`;
    }

    if (activeLang === "Python") {
      return `class LiaoEngine:
    async def optimize_core(self):
        await connect("SADIK_NODE")`;
    }

    return `SELECT *
FROM users
WHERE status = 'active'
ORDER BY created_at DESC;`;
  }, [activeLang]);

  const handleAction = () => {
    setIsAnalyzing(true);

    setTimeout(() => {
      setIsAnalyzing(false);
    }, 2200);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(generatedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch (error) {}
  };

  const handleClear = () => {
    setPrompt("");
  };

  return (
    <div className="relative h-full w-full overflow-hidden bg-[#02040A] text-white p-6 lg:p-8 flex flex-col gap-6">

      {/* Ambient */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.015]" />
        <div className="absolute top-[-80px] right-[-50px] h-72 w-72 rounded-full bg-cyan-500/10 blur-[120px]" />
        <div className="absolute bottom-[-120px] left-[-80px] h-72 w-72 rounded-full bg-blue-500/10 blur-[120px]" />
      </div>

      {/* Top Bar */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-4 rounded-3xl border border-white/5 bg-white/[0.02] p-4 backdrop-blur-xl">

        <div className="flex flex-wrap items-center gap-5">

          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-cyan-500/10 p-2">
              <Terminal size={18} className="text-cyan-400" />
            </div>

            <div>
              <h2 className="text-[11px] font-black uppercase tracking-[0.28em] text-slate-300">
                Neural Code Engine
              </h2>
              <p className="text-[10px] text-slate-500 uppercase tracking-wider">
                Adaptive Generation System
              </p>
            </div>
          </div>

          <div className="hidden h-6 w-px bg-white/10 lg:block" />

          <div className="flex flex-wrap gap-2">
            {languages.map((lang) => {
              const Icon = lang.icon;
              const active = activeLang === lang.name;

              return (
                <button
                  key={lang.name}
                  onClick={() => setActiveLang(lang.name)}
                  className={`px-4 py-2 rounded-full text-[10px] font-bold uppercase tracking-wide transition-all flex items-center gap-2 ${
                    active
                      ? "bg-white/10 border border-white/15 text-white"
                      : "text-slate-500 hover:text-slate-200 hover:bg-white/[0.03]"
                  }`}
                >
                  <Icon size={12} className={lang.color} />
                  {lang.name}
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex items-center gap-2">

          <button
            onClick={handleCopy}
            className="rounded-xl p-2.5 text-slate-500 hover:bg-white/5 hover:text-cyan-400 transition"
          >
            {copied ? <Check size={16} /> : <Copy size={16} />}
          </button>

          <button
            className="rounded-xl p-2.5 text-slate-500 hover:bg-white/5 hover:text-white transition"
          >
            <Download size={16} />
          </button>

          <button
            onClick={handleAction}
            className="flex items-center gap-2 rounded-xl bg-cyan-500 px-5 py-2.5 text-[10px] font-black uppercase tracking-wider text-black shadow-[0_0_25px_rgba(34,211,238,0.28)] hover:bg-cyan-400 transition"
          >
            {isAnalyzing ? (
              <Cpu size={14} className="animate-spin" />
            ) : (
              <Wand2 size={14} />
            )}

            {isAnalyzing ? "Processing..." : "Generate"}
          </button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="relative z-10 grid flex-1 grid-cols-1 gap-6 overflow-hidden xl:grid-cols-2">

        {/* Prompt Panel */}
        <div className="flex flex-col overflow-hidden rounded-[30px] border border-white/5 bg-white/[0.015]">

          <div className="flex items-center justify-between border-b border-white/5 bg-white/[0.02] p-4">
            <span className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.22em] text-slate-500">
              <Brackets size={12} />
              Prompt Input
            </span>

            <button
              onClick={handleClear}
              className="rounded-lg p-2 text-slate-600 hover:bg-white/5 hover:text-red-400 transition"
            >
              <Trash2 size={14} />
            </button>
          </div>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your project... e.g. Build secure auth API in C# with SQL Server"
            className="flex-1 resize-none bg-transparent p-6 font-mono text-sm leading-relaxed text-slate-300 outline-none placeholder:text-slate-700"
          />

          <div className="border-t border-white/5 px-6 py-3 text-[10px] uppercase tracking-widest text-slate-600">
            Smart parsing enabled
          </div>
        </div>

        {/* Output Panel */}
        <div className="relative flex flex-col overflow-hidden rounded-[30px] border border-cyan-500/10 bg-[#05070F] shadow-inner">

          <div className="pointer-events-none absolute right-0 top-0 h-36 w-36 bg-cyan-500/10 blur-3xl" />

          <div className="flex items-center justify-between border-b border-white/5 p-4">
            <div className="flex items-center gap-3">
              <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-400" />
              <span className="text-[10px] font-black uppercase tracking-[0.22em] text-cyan-400">
                Output Engine
              </span>
            </div>

            <button className="text-slate-600 hover:text-emerald-400 transition">
              <Play size={14} />
            </button>
          </div>

          <div className="flex-1 overflow-auto p-6 custom-scrollbar">
            <AnimatePresence mode="wait">
              <motion.pre
                key={activeLang + isAnalyzing}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="font-mono text-sm leading-7 text-slate-300 whitespace-pre-wrap"
              >
                {isAnalyzing ? "Generating optimized solution..." : generatedCode}
              </motion.pre>
            </AnimatePresence>
          </div>

          <div className="border-t border-white/5 px-6 py-3 flex items-center justify-between text-[10px] uppercase tracking-widest">
            <span className="text-slate-600">Compiled Preview Ready</span>
            <span className="text-cyan-500">Secure Mode</span>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-4 px-1 opacity-70">

        <div className="flex flex-wrap gap-5 text-[10px] font-mono uppercase text-slate-500">
          <span className="flex items-center gap-2">
            <Globe size={10} />
            Latency 0.04s
          </span>

          <span className="flex items-center gap-2">
            <Cpu size={10} />
            Tokens 1.2k/s
          </span>

          <span className="flex items-center gap-2">
            <Zap size={10} />
            GPU Ready
          </span>
        </div>

        <div className="text-[10px] font-mono uppercase tracking-widest text-cyan-500">
          AES-256 Encrypted
        </div>
      </div>
    </div>
  );
}