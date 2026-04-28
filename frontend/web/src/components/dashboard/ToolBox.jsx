import React, { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Wrench,
  Layers,
  Hash,
  Calculator,
  Settings2,
  Box,
  ExternalLink,
  Code2,
  Palette,
  Zap,
  Cpu,
  ArrowRight,
  Search,
  Shield,
  Database,
  Sparkles,
  Gauge,
  Workflow,
  TerminalSquare,
  Lock,
  CheckCircle2,
} from "lucide-react";

export default function ToolBox() {
  const [activeCategory, setActiveCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [selectedTool, setSelectedTool] = useState("JSON Formatter");

  const tools = [
    {
      name: "JSON Formatter",
      desc: "Validate, compress & beautify structured payloads",
      icon: Code2,
      color: "text-cyan-400",
      category: "Dev",
      status: "Stable",
      load: 82,
    },
    {
      name: "Color Lab",
      desc: "Generate premium UI palettes instantly",
      icon: Palette,
      color: "text-fuchsia-400",
      category: "Design",
      status: "Online",
      load: 64,
    },
    {
      name: "Hash Generator",
      desc: "SHA / AES utility encryption engine",
      icon: Hash,
      color: "text-emerald-400",
      category: "Security",
      status: "Secured",
      load: 90,
    },
    {
      name: "Logic Units",
      desc: "Scientific calculator & unit matrix",
      icon: Calculator,
      color: "text-amber-400",
      category: "Dev",
      status: "Ready",
      load: 72,
    },
    {
      name: "Grid Engine",
      desc: "CSS grid & responsive layout builder",
      icon: Layers,
      color: "text-pink-400",
      category: "Design",
      status: "Active",
      load: 58,
    },
    {
      name: "API Tester",
      desc: "Inspect backend endpoints & latency",
      icon: Zap,
      color: "text-blue-400",
      category: "Dev",
      status: "Live",
      load: 88,
    },
    {
      name: "Vault Scanner",
      desc: "Permission & token analyzer",
      icon: Shield,
      color: "text-violet-400",
      category: "Security",
      status: "Protected",
      load: 76,
    },
    {
      name: "DB Forge",
      desc: "SQL schema assistant & optimizer",
      icon: Database,
      color: "text-sky-400",
      category: "Dev",
      status: "Stable",
      load: 69,
    },
  ];

  const filteredTools = useMemo(() => {
    return tools.filter((tool) => {
      const byCategory =
        activeCategory === "All" || tool.category === activeCategory;

      const bySearch =
        tool.name.toLowerCase().includes(search.toLowerCase()) ||
        tool.desc.toLowerCase().includes(search.toLowerCase());

      return byCategory && bySearch;
    });
  }, [activeCategory, search]);

  const currentTool =
    tools.find((tool) => tool.name === selectedTool) || tools[0];

  return (
    <div className="relative h-full w-full overflow-hidden bg-[#02040A] text-white">
      {/* Ambient Layer */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute right-[-80px] top-[-40px] h-72 w-72 rounded-full bg-fuchsia-500/10 blur-[120px]" />
        <div className="absolute left-[-90px] bottom-[-40px] h-72 w-72 rounded-full bg-cyan-500/10 blur-[120px]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.03),transparent_35%)]" />
      </div>

      <div className="relative z-10 flex h-full flex-col overflow-hidden p-6 lg:p-8">
        {/* Header */}
        <div className="rounded-[32px] border border-white/5 bg-white/[0.02] p-5 backdrop-blur-2xl">
          <div className="flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 rounded-2xl bg-fuchsia-500/30 blur-xl" />
                <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.04]">
                  <Wrench size={22} className="text-fuchsia-400" />
                </div>
              </div>

              <div>
                <h1 className="text-sm font-black uppercase tracking-[0.45em] text-slate-300">
                  Neural Toolbox
                </h1>
                <p className="mt-1 text-[10px] font-mono uppercase tracking-[0.25em] text-slate-500">
                  Jarvis Utility Matrix // 8 Modules Loaded
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              <MetricCard
                icon={Cpu}
                label="Engine"
                value="99.2%"
                color="text-cyan-400"
              />
              <MetricCard
                icon={Gauge}
                label="Latency"
                value="04ms"
                color="text-emerald-400"
              />
              <MetricCard
                icon={Workflow}
                label="Threads"
                value="128"
                color="text-amber-400"
              />
              <MetricCard
                icon={Lock}
                label="Secure"
                value="ON"
                color="text-violet-400"
              />
            </div>
          </div>
        </div>

        {/* Body */}
        <div className="mt-6 grid min-h-0 flex-1 grid-cols-1 gap-6 xl:grid-cols-12">
          {/* Left Panel */}
          <div className="xl:col-span-8 flex min-h-0 flex-col rounded-[32px] border border-white/5 bg-white/[0.015] p-5 backdrop-blur-2xl">
            {/* Search + Filter */}
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div className="relative w-full lg:max-w-md">
                <Search
                  size={16}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600"
                />
                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search utility module..."
                  className="h-12 w-full rounded-2xl border border-white/5 bg-white/[0.03] pl-11 pr-4 text-sm outline-none transition-all placeholder:text-slate-700 focus:border-cyan-500/30"
                />
              </div>

              <div className="flex flex-wrap gap-2">
                {["All", "Dev", "Design", "Security"].map((cat) => {
                  const active = activeCategory === cat;

                  return (
                    <button
                      key={cat}
                      onClick={() => setActiveCategory(cat)}
                      className={`rounded-full px-5 py-2 text-[10px] font-black uppercase tracking-[0.25em] transition-all ${
                        active
                          ? "bg-white/10 text-white border border-white/15"
                          : "text-slate-500 hover:text-slate-300"
                      }`}
                    >
                      {cat}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Grid */}
            <div className="mt-5 min-h-0 flex-1 overflow-y-auto pr-1">
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <AnimatePresence>
                  {filteredTools.map((tool, idx) => {
                    const Icon = tool.icon;
                    const active = selectedTool === tool.name;

                    return (
                      <motion.button
                        layout
                        key={tool.name}
                        initial={{ opacity: 0, y: 16 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -16 }}
                        transition={{ delay: idx * 0.03 }}
                        whileHover={{ y: -4, scale: 1.01 }}
                        onClick={() => setSelectedTool(tool.name)}
                        className={`group relative overflow-hidden rounded-[28px] border p-5 text-left transition-all ${
                          active
                            ? "border-cyan-500/20 bg-white/[0.04]"
                            : "border-white/5 bg-white/[0.015] hover:border-white/10"
                        }`}
                      >
                        <div className="absolute right-0 top-0 h-24 w-24 rounded-full bg-white/5 blur-3xl" />

                        <div className="relative z-10 flex items-start justify-between">
                          <div
                            className={`rounded-2xl bg-white/5 p-3 ${tool.color}`}
                          >
                            <Icon size={20} />
                          </div>

                          <ExternalLink
                            size={15}
                            className="text-slate-700 transition-colors group-hover:text-slate-400"
                          />
                        </div>

                        <div className="relative z-10 mt-4">
                          <h3 className="text-xs font-black uppercase tracking-[0.18em] text-slate-200">
                            {tool.name}
                          </h3>

                          <p className="mt-2 text-[10px] uppercase tracking-wide text-slate-600">
                            {tool.desc}
                          </p>
                        </div>

                        <div className="relative z-10 mt-5 flex items-center justify-between gap-3">
                          <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/5">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${tool.load}%` }}
                              transition={{ duration: 0.8 }}
                              className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500"
                            />
                          </div>

                          <span className="text-[9px] font-mono text-slate-500">
                            {tool.load}%
                          </span>
                        </div>
                      </motion.button>
                    );
                  })}
                </AnimatePresence>
              </div>
            </div>
          </div>

          {/* Right Panel */}
          <div className="xl:col-span-4 flex min-h-0 flex-col gap-6">
            {/* Inspector */}
            <div className="rounded-[32px] border border-white/5 bg-white/[0.02] p-5 backdrop-blur-2xl">
              <div className="flex items-center justify-between">
                <h2 className="text-[11px] font-black uppercase tracking-[0.35em] text-slate-500">
                  Module Inspector
                </h2>

                <Sparkles size={14} className="text-cyan-400" />
              </div>

              <div className="mt-5 rounded-[26px] border border-white/5 bg-[#060A12] p-5">
                <div className="flex items-center gap-4">
                  <div
                    className={`rounded-2xl bg-white/5 p-3 ${currentTool.color}`}
                  >
                    <currentTool.icon size={22} />
                  </div>

                  <div>
                    <h3 className="text-sm font-black uppercase tracking-wide">
                      {currentTool.name}
                    </h3>
                    <p className="text-[10px] uppercase tracking-widest text-slate-600">
                      {currentTool.category} Utility
                    </p>
                  </div>
                </div>

                <p className="mt-5 text-[11px] leading-relaxed text-slate-400">
                  {currentTool.desc}
                </p>

                <div className="mt-5 grid grid-cols-2 gap-3">
                  <MiniStat label="Status" value={currentTool.status} />
                  <MiniStat label="Runtime" value="Stable" />
                  <MiniStat label="Threads" value="32" />
                  <MiniStat label="Version" value="v2.1" />
                </div>

                <button className="mt-5 flex w-full items-center justify-center gap-2 rounded-2xl bg-cyan-500 py-3 text-[10px] font-black uppercase tracking-[0.25em] text-black transition-all hover:bg-cyan-400 active:scale-[0.98]">
                  Launch Module <ArrowRight size={14} />
                </button>
              </div>
            </div>

            {/* Logs */}
            <div className="min-h-0 flex-1 rounded-[32px] border border-white/5 bg-white/[0.015] p-5 backdrop-blur-2xl">
              <div className="flex items-center justify-between">
                <h2 className="text-[11px] font-black uppercase tracking-[0.35em] text-slate-500">
                  Activity Feed
                </h2>

                <TerminalSquare size={14} className="text-emerald-400" />
              </div>

              <div className="mt-5 space-y-3 overflow-y-auto pr-1">
                {[
                  "JSON Formatter synchronized.",
                  "Vault Scanner token check passed.",
                  "API Tester latency reduced to 04ms.",
                  "Color Lab palette cache refreshed.",
                  "DB Forge optimization complete.",
                ].map((item, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: 12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="flex items-start gap-3 rounded-2xl border border-white/5 bg-white/[0.02] p-3"
                  >
                    <CheckCircle2
                      size={15}
                      className="mt-0.5 shrink-0 text-emerald-400"
                    />
                    <p className="text-[10px] uppercase tracking-wide text-slate-400">
                      {item}
                    </p>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex items-center justify-between rounded-2xl border border-white/5 bg-white/[0.015] px-5 py-4">
          <div className="flex flex-wrap gap-5 text-[10px] font-mono uppercase text-slate-500">
            <span className="flex items-center gap-2">
              <Cpu size={12} />
              Neural Core Stable
            </span>

            <span className="flex items-center gap-2">
              <Box size={12} />
              Container Isolated
            </span>
          </div>

          <button className="rounded-xl p-2 text-slate-600 transition-all hover:bg-white/5 hover:text-fuchsia-400">
            <Settings2 size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}

/* Helper Components */

function MetricCard({ icon: Icon, label, value, color }) {
  return (
    <div className="rounded-2xl border border-white/5 bg-white/[0.02] px-4 py-3">
      <div className="flex items-center gap-2">
        <Icon size={13} className={color} />
        <span className="text-[9px] font-black uppercase tracking-[0.22em] text-slate-600">
          {label}
        </span>
      </div>

      <p className={`mt-2 text-sm font-black ${color}`}>{value}</p>
    </div>
  );
}

function MiniStat({ label, value }) {
  return (
    <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-3">
      <p className="text-[9px] font-black uppercase tracking-[0.22em] text-slate-600">
        {label}
      </p>
      <p className="mt-1 text-[11px] font-bold text-slate-300">{value}</p>
    </div>
  );
}