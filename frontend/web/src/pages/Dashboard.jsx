import React from "react";
import { motion } from "framer-motion";
import {
  Activity, MessageCircle, Mic, Cpu, Zap, Settings, Brain, 
  ArrowUpRight, ShieldCheck, Terminal, Layers, History, Workflow,
  Dna, Plus, Sparkles
} from "lucide-react";

export default function Dashboard() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="h-full w-full p-6 text-white overflow-y-auto custom-scrollbar bg-transparent">
      
      {/* 1. HEADER SECTION (Optimized - Time Removed) */}
      <motion.div 
        initial={{ opacity: 0, x: -20 }} 
        animate={{ opacity: 1, x: 0 }} 
        className="mb-10"
      >
        <div className="flex items-center gap-2 mb-2">
          <div className="h-2 w-2 rounded-full bg-cyan-500 animate-pulse shadow-[0_0_10px_#22d3ee]" />
          <span className="text-[10px] font-bold uppercase tracking-[4px] text-cyan-500/80">Neural Link Active</span>
        </div>
        <h1 className="text-3xl md:text-5xl font-black tracking-tighter bg-gradient-to-r from-white via-slate-200 to-slate-500 bg-clip-text text-transparent">
          Welcome, Sadik
        </h1>
        <p className="text-slate-400 text-sm font-medium mt-1">Lì Ào Engine v3.0.2 • System Monitoring Online</p>
      </motion.div>

      {/* 2. STATS GRID */}
      <motion.div 
        variants={containerVariants} 
        initial="hidden" 
        animate="visible" 
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10"
      >
        <StatCard icon={Cpu} label="Neural Load" value="14%" subValue="Optimized" color="cyan" />
        <StatCard icon={History} label="Operations" value="1,284" subValue="+12% today" color="purple" />
        <StatCard icon={ShieldCheck} label="Security" value="Encrypted" subValue="Protocol 7" color="green" />
        <StatCard icon={Zap} label="Latency" value="12ms" subValue="Ultra Fast" color="yellow" />
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
        
        {/* LEFT COLUMN: ACTIONS & TRAINING */}
        <motion.div variants={itemVariants} className="lg:col-span-2 space-y-8">
          
          {/* QUICK COMMAND CENTER */}
          <section>
            <div className="flex items-center justify-between px-1 mb-4">
              <h2 className="text-xs font-bold uppercase tracking-widest text-slate-500">Quick Command Center</h2>
              <div className="h-px flex-1 bg-white/5 mx-4" />
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <ActionButton icon={MessageCircle} label="Deep Chat" sub="AI 4.0" />
              <ActionButton icon={Mic} label="Voice Link" sub="Active" />
              <ActionButton icon={Terminal} label="Terminal" sub="Root" />
              <ActionButton icon={Workflow} label="Automate" sub="Tasks" />
            </div>
          </section>

          {/* 🧠 NEURAL TRAINING HUB */}
          <section>
            <div className="flex items-center justify-between px-1 mb-4">
              <h2 className="text-xs font-bold uppercase tracking-widest text-cyan-500/70">Neural Training Hub</h2>
              <div className="h-px flex-1 bg-cyan-500/10 mx-4" />
            </div>
            <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6 backdrop-blur-xl group hover:border-cyan-500/40 transition-all duration-500">
              <div className="flex flex-col md:flex-row gap-6 items-center">
                <div className="relative">
                   <div className="absolute inset-0 bg-cyan-500/20 blur-2xl rounded-full animate-pulse" />
                   <div className="relative h-20 w-20 rounded-2xl bg-gradient-to-br from-[#0A0C16] to-[#1E293B] border border-cyan-500/30 flex items-center justify-center shadow-2xl">
                      <Dna className="text-cyan-400 animate-bounce" size={36} />
                   </div>
                </div>
                <div className="flex-1 text-center md:text-left">
                  <h3 className="text-lg font-bold text-white mb-2 flex items-center justify-center md:justify-start gap-2">
                    Train Lì Ào Intelligence
                    <Sparkles size={16} className="text-yellow-400" />
                  </h3>
                  <p className="text-sm text-slate-400 max-w-md">
                    Upload your custom datasets or documents to fine-tune your personal AI model for better precision.
                  </p>
                </div>
                <button className="px-6 py-3 rounded-xl bg-cyan-500 text-[#02040A] font-bold text-sm flex items-center gap-2 hover:bg-cyan-400 transition-colors shadow-[0_0_20px_rgba(34,211,238,0.3)]">
                  <Plus size={18} />
                  Start Training
                </button>
              </div>
            </div>
          </section>

          {/* INSIGHT PANEL */}
          <div className="rounded-2xl border border-white/5 bg-[#0A0C16]/40 p-5 backdrop-blur-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Layers size={80} />
            </div>
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Activity size={18} className="text-cyan-500" />
              AI Insight Engine
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed max-w-xl">
               System synchronized. Backend services responding at <span className="text-emerald-400 font-mono text-xs">Peak Performance</span>. HCI layers fully optimized.
            </p>
          </div>
        </motion.div>

        {/* RIGHT COLUMN: ACTIVITY FEED */}
        <motion.div variants={itemVariants} className="rounded-2xl border border-white/5 bg-[#0A0C16]/20 p-5">
          <h2 className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-6">Recent Activity</h2>
          <div className="space-y-6">
            <ActivityItem time="2m ago" title="Voice Training" desc="Updated speech patterns" active={true} />
            <ActivityItem time="1h ago" title="Dataset Loaded" desc="2.4GB tech logs ingested" active={false} />
            <ActivityItem time="4h ago" title="UI Update" desc="Sidebar architecture fixed" />
            <ActivityItem time="Yesterday" title="System Backup" desc="Cloud sync completed" />
          </div>
        </motion.div>

      </div>
    </div>
  );
}

// Helper Components
function StatCard({ icon: Icon, label, value, subValue, color }) {
  const colorStyles = {
    cyan: "from-cyan-500/20 to-transparent border-cyan-500/20 text-cyan-400",
    purple: "from-purple-500/20 to-transparent border-purple-500/20 text-purple-400",
    green: "from-emerald-500/20 to-transparent border-emerald-500/20 text-emerald-400",
    yellow: "from-yellow-500/20 to-transparent border-yellow-500/20 text-yellow-400",
  };
  return (
    <div className={`relative p-5 rounded-2xl bg-gradient-to-br ${colorStyles[color]} border backdrop-blur-sm group hover:scale-[1.02] transition-all duration-300`}>
      <div className="flex justify-between items-start mb-4">
        <div className={`p-2 rounded-lg bg-white/5 ${colorStyles[color].split(' ').pop()}`}><Icon size={20} /></div>
        <ArrowUpRight size={14} className="text-slate-600 group-hover:text-white transition-colors" />
      </div>
      <div>
        <p className="text-xs font-bold text-slate-500 uppercase tracking-tighter mb-1">{label}</p>
        <div className="flex items-baseline gap-2">
          <h3 className="text-2xl font-black text-white">{value}</h3>
          <span className="text-[10px] font-medium text-slate-500">{subValue}</span>
        </div>
      </div>
    </div>
  );
}

function ActionButton({ icon: Icon, label, sub }) {
  return (
    <button className="group relative p-4 rounded-2xl bg-white/[0.03] border border-white/5 hover:border-cyan-500/30 hover:bg-white/[0.06] transition-all duration-300 flex flex-col items-center gap-3 overflow-hidden w-full">
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      <Icon size={22} className="text-slate-400 group-hover:text-cyan-400 transition-colors duration-300" />
      <div className="text-center">
        <p className="text-xs font-bold text-white tracking-tight">{label}</p>
        <p className="text-[9px] font-medium text-slate-500 uppercase">{sub}</p>
      </div>
    </button>
  );
}

function ActivityItem({ time, title, desc, active }) {
  return (
    <div className="flex gap-4">
      <div className="flex flex-col items-center">
        <div className={`h-2 w-2 rounded-full ${active ? 'bg-cyan-500 shadow-[0_0_8px_#22d3ee]' : 'bg-slate-700'}`} />
        <div className="w-px flex-1 bg-white/5 my-1" />
      </div>
      <div>
        <div className="flex items-center gap-2">
          <h4 className="text-sm font-bold text-slate-200">{title}</h4>
          <span className="text-[9px] font-mono text-slate-600 uppercase">{time}</span>
        </div>
        <p className="text-xs text-slate-500">{desc}</p>
      </div>
    </div>
  );
}