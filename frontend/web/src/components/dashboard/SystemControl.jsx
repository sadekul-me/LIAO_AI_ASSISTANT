import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Shield,
  Power,
  Wifi,
  Cpu,
  Lock,
  RefreshCw,
  Activity,
  Server,
  Zap,
  Brain,
  Radio,
} from "lucide-react";

export default function SystemControl() {
  const [online, setOnline] = useState(true);
  const [secure, setSecure] = useState(true);
  const [boost, setBoost] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleOptimize = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2200);
  };

  const cards = [
    {
      title: "Core Status",
      value: online ? "Active" : "Hibernate",
      icon: Power,
      color: "text-cyan-400",
      fill: "bg-cyan-500",
      glow: "bg-cyan-500/10",
      progress: online ? 88 : 12,
    },
    {
      title: "Security",
      value: secure ? "Encrypted" : "Warning",
      icon: Lock,
      color: "text-purple-400",
      fill: "bg-purple-500",
      glow: "bg-purple-500/10",
      progress: secure ? 96 : 30,
    },
    {
      title: "Network",
      value: online ? "1.2 Gbps" : "Offline",
      icon: Wifi,
      color: "text-blue-400",
      fill: "bg-blue-500",
      glow: "bg-blue-500/10",
      progress: online ? 78 : 5,
    },
    {
      title: "Neural Mode",
      value: boost ? "Overclock" : "Optimal",
      icon: Brain,
      color: "text-amber-400",
      fill: "bg-amber-500",
      glow: "bg-amber-500/10",
      progress: boost ? 100 : 64,
    },
  ];

  return (
    <div className="relative h-full w-full overflow-hidden bg-[#02040A] text-white p-6 lg:p-8 flex flex-col gap-6">

      {/* Background */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.015]" />
        <div className="absolute top-[-120px] right-[-80px] h-80 w-80 rounded-full bg-cyan-500/10 blur-[140px]" />
        <div className="absolute bottom-[-140px] left-[-80px] h-80 w-80 rounded-full bg-blue-500/10 blur-[140px]" />
      </div>

      {/* Header */}
      <div className="relative z-10 rounded-[30px] border border-white/5 bg-white/[0.02] backdrop-blur-2xl px-6 py-5 flex items-center justify-between overflow-hidden">

        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 via-transparent to-transparent" />

        <div className="relative z-10 flex items-center gap-4">
          <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-4 shadow-[0_0_25px_rgba(34,211,238,0.12)]">
            <Shield className="text-cyan-400" size={22} />
          </div>

          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.35em] text-slate-500">
              System Control
            </p>

            <div className="mt-1 flex items-center gap-3">
              <h1 className="text-lg font-bold tracking-tight">
                LÌ ÀO PROTOCOL
              </h1>

              <span className="rounded-md bg-cyan-500 px-2 py-0.5 text-[10px] font-black text-black">
                v1.0.0
              </span>
            </div>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-5 relative z-10">
          <div className="text-right">
            <p className="text-[10px] uppercase text-slate-500 font-black">
              Node Status
            </p>
            <p className="text-xs font-mono text-emerald-400">
              NOMINAL_READY
            </p>
          </div>

          <div className="h-10 w-px bg-white/10" />

          <Radio
            size={18}
            className={`${online ? "text-cyan-400 animate-pulse" : "text-slate-600"}`}
          />
        </div>
      </div>

      {/* Metrics */}
      <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {cards.map((item, idx) => {
          const Icon = item.icon;

          return (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.08 }}
              whileHover={{ y: -5, scale: 1.015 }}
              className="rounded-[28px] border border-white/5 bg-white/[0.015] p-5 overflow-hidden relative"
            >
              <div className={`absolute top-0 right-0 h-24 w-24 rounded-full blur-3xl ${item.glow}`} />

              <div className="relative z-10 flex items-center justify-between">
                <span className="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-black">
                  {item.title}
                </span>

                <Icon size={18} className={item.color} />
              </div>

              <div className="relative z-10 mt-5 text-2xl font-black tracking-tight">
                {item.value}
              </div>

              <div className="mt-4 h-1.5 w-full rounded-full bg-white/5 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${item.progress}%` }}
                  transition={{ duration: 1.1, delay: idx * 0.1 }}
                  className={`h-full rounded-full ${item.fill}`}
                />
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Main Panels */}
      <div className="relative z-10 grid flex-1 min-h-0 grid-cols-1 xl:grid-cols-5 gap-6">

        {/* Controls */}
        <div className="xl:col-span-2 rounded-[34px] border border-white/5 bg-white/[0.015] p-7 flex flex-col gap-4 overflow-hidden">

          <h2 className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 mb-1">
            Manual Overrides
          </h2>

          <ToggleButton
            label="Core Power"
            active={online}
            onClick={() => setOnline(!online)}
            color="cyan"
          />

          <ToggleButton
            label="Neural Firewall"
            active={secure}
            onClick={() => setSecure(!secure)}
            color="purple"
          />

          <ToggleButton
            label="Turbo Boost"
            active={boost}
            onClick={() => setBoost(!boost)}
            color="amber"
          />

          <button
            onClick={handleOptimize}
            disabled={loading}
            className="mt-auto rounded-2xl py-4 bg-cyan-500 text-black font-black text-[11px] uppercase tracking-[0.2em] flex items-center justify-center gap-3 hover:bg-cyan-400 transition active:scale-[0.98] disabled:opacity-60 shadow-[0_0_25px_rgba(34,211,238,0.22)]"
          >
            {loading ? (
              <RefreshCw size={16} className="animate-spin" />
            ) : (
              <Zap size={16} fill="currentColor" />
            )}

            {loading ? "Re-Indexing..." : "Optimize Neural Core"}
          </button>
        </div>

        {/* Telemetry */}
        <div className="xl:col-span-3 rounded-[34px] border border-white/5 bg-[#03060E] p-7 flex flex-col gap-6 overflow-hidden relative">

          <div className="absolute top-0 right-0 h-40 w-40 bg-cyan-500/5 blur-[110px]" />

          <div className="relative z-10 flex items-center justify-between">
            <h2 className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">
              Node Analytics
            </h2>

            <Activity size={14} className="text-cyan-500 animate-pulse" />
          </div>

          <div className="relative z-10 space-y-6">
            <TelemetryRow
              label="Thread Allocation"
              value="128 Unit"
              sub="Stable"
              progress={72}
              color="bg-cyan-500"
            />

            <TelemetryRow
              label="Memory Occupancy"
              value="4.2 GB"
              sub="42%"
              progress={42}
              color="bg-purple-500"
            />

            <TelemetryRow
              label="Sync Latency"
              value="12 ms"
              sub="Fast"
              progress={18}
              color="bg-emerald-500"
            />

            <TelemetryRow
              label="Compute Throughput"
              value="91%"
              sub="High"
              progress={91}
              color="bg-amber-500"
            />
          </div>

          <div className="mt-auto rounded-2xl border border-cyan-500/10 bg-cyan-500/[0.03] p-5 flex items-center gap-4 border-l-4 border-l-cyan-500 relative z-10">
            <div className="rounded-xl bg-cyan-500/10 p-2 text-cyan-400">
              <Server size={18} />
            </div>

            <p className="text-[11px] leading-relaxed text-slate-300">
              <span className="font-bold text-cyan-400 uppercase">
                System Update:
              </span>{" "}
              Neural Engine is operating at peak stability. No anomalies detected.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

/* Toggle */
function ToggleButton({ label, active, onClick, color }) {
  const colors = {
    cyan: "text-cyan-400 border-cyan-500/20 bg-cyan-500/10",
    purple: "text-purple-400 border-purple-500/20 bg-purple-500/10",
    amber: "text-amber-400 border-amber-500/20 bg-amber-500/10",
  };

  return (
    <button
      onClick={onClick}
      className={`rounded-2xl border px-5 py-4 flex items-center justify-between transition-all ${
        active
          ? colors[color]
          : "border-white/5 bg-white/[0.02] text-slate-500 hover:border-white/10"
      }`}
    >
      <span className="text-[11px] uppercase tracking-[0.15em] font-bold">
        {label}
      </span>

      <div
        className={`relative h-5 w-10 rounded-full transition ${
          active ? "bg-current" : "bg-white/10"
        }`}
      >
        <motion.div
          animate={{ x: active ? 22 : 2 }}
          transition={{ type: "spring", stiffness: 260, damping: 18 }}
          className="absolute top-1 h-3 w-3 rounded-full bg-white shadow-lg"
        />
      </div>
    </button>
  );
}

/* Telemetry */
function TelemetryRow({ label, value, sub, progress, color }) {
  return (
    <div>
      <div className="mb-2 flex items-end justify-between">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-[0.08em] text-slate-200">
            {label}
          </p>
          <p className="text-[9px] font-mono uppercase text-slate-600">
            {sub}
          </p>
        </div>

        <span className="text-xs font-mono font-bold text-slate-400">
          {value}
        </span>
      </div>

      <div className="h-1.5 w-full rounded-full bg-white/5 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 1 }}
          className={`h-full rounded-full ${color}`}
        />
      </div>
    </div>
  );
}