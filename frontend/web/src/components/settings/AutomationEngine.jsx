import React, { useState } from 'react';
import { motion, AnimatePresence } from "framer-motion";
import { 
  Cpu, Zap, Activity, Clock, Terminal, 
  Workflow, Brain, Shield, Trash2, Code, 
  Settings, ChevronRight, Play, Pause 
} from "lucide-react";

export default function AutomationEngine() {
  const [activeTasks] = useState(12);

  // সব আইকন এখানে সঠিকভাবে ম্যাপ করা হয়েছে
  const routines = [
    { id: 1, name: "Neural Sync", status: "Active", load: "24%", icon: Brain },
    { id: 2, name: "Auto-Dev Mode", status: "Idle", load: "0%", icon: Code },
    { id: 3, name: "Security Perimeter", status: "Active", load: "12%", icon: Shield },
    { id: 4, name: "Resource Sweep", status: "Active", load: "45%", icon: Trash2 },
  ];

  return (
    <div className="h-full w-full bg-[#050914] text-white p-8 lg:p-12 flex flex-col gap-10 overflow-hidden relative">
      
      {/* 🌌 BACKGROUND EFFECTS */}
      <div className="absolute inset-0 pointer-events-none opacity-20">
        <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-cyan-500/10 blur-[150px] rounded-full" />
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.02]" />
      </div>

      {/* 🛰️ TOP DASHBOARD: REAL-TIME METRICS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative z-10">
        <MetricCard label="Active Routines" value={activeTasks} sub="Total Processes" icon={Workflow} color="text-cyan-400" />
        <MetricCard label="Latency" value="12ms" sub="Ultra-Fast Sync" icon={Clock} color="text-purple-400" />
        <MetricCard label="Core Load" value="38%" sub="Optimized" icon={Activity} color="text-emerald-400" />
        <MetricCard label="Hardware ID" value="SADIK_2026" sub="Verified Node" icon={Cpu} color="text-amber-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 flex-1 relative z-10 overflow-hidden">
        
        {/* 🛠️ LEFT: AUTOMATION CONTROL CENTER */}
        <div className="lg:col-span-8 flex flex-col gap-8 overflow-hidden">
          <SectionHeader title="Active Command Sequences" icon={Terminal} />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 overflow-y-auto pr-2 custom-scrollbar">
            {routines.map((item) => (
              <AutomationCard key={item.id} data={item} />
            ))}
          </div>

          {/* SYSTEM LOG OVERRIDE */}
          <div className="mt-auto p-6 bg-white/[0.02] border border-white/5 rounded-3xl backdrop-blur-md">
            <div className="flex justify-between items-center mb-4">
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">System Log // Live Output</span>
              <div className="flex gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-cyan-500 animate-pulse" />
                <div className="h-1.5 w-1.5 rounded-full bg-cyan-500/40 animate-pulse delay-75" />
              </div>
            </div>
            <div className="font-mono text-[9px] text-cyan-400/60 space-y-1">
              <p>{`> [${new Date().toLocaleTimeString()}] AUTH_TOKEN_VALIDATED: SADIK_ENG_NODE`}</p>
              <p>{`> [${new Date().toLocaleTimeString()}] AUTOMATION_FLOW_INITIATED: LÌ ÀO ENGINE V3.0`}</p>
              <p className="text-emerald-400/80">{`> [${new Date().toLocaleTimeString()}] ALL_SYSTEMS_OPERATIONAL: STABLE`}</p>
            </div>
          </div>
        </div>

        {/* ⚙️ RIGHT: GLOBAL AUTOMATION LOGIC */}
        <div className="lg:col-span-4 space-y-8">
          <SectionHeader title="Override Parameters" icon={Settings} />
          
          <div className="space-y-4">
            <ControlToggle label="Auto-Optimization" desc="Self-healing system logic" active={true} />
            <ControlToggle label="Dynamic Scaling" desc="Adjust resources based on load" active={false} />
            <ControlToggle label="Ghost Protocol" desc="Execute tasks in stealth mode" active={true} />
          </div>

          <div className="p-8 bg-gradient-to-br from-cyan-500/10 to-transparent border border-cyan-400/20 rounded-[40px] text-center relative overflow-hidden group">
            <div className="absolute inset-0 bg-cyan-400/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <Zap className="text-cyan-400 mx-auto mb-4 animate-bounce" size={32} />
            <h4 className="text-xs font-black uppercase tracking-[4px] relative z-10">Ultra Sync Enabled</h4>
            <p className="text-[9px] text-slate-500 mt-2 leading-relaxed relative z-10">
              System is running at maximum efficiency. All background tasks are synchronized with the Lì Ào Protocol core.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

// --- Internal Specialized Components ---

function MetricCard({ label, value, sub, icon: Icon, color }) {
  return (
    <div className="p-6 bg-white/[0.02] border border-white/5 rounded-3xl hover:border-white/10 transition-all group cursor-default">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-xl bg-white/5 ${color} group-hover:scale-110 transition-transform duration-300`}>
          <Icon size={20} />
        </div>
        <div className="h-1 w-8 bg-white/5 rounded-full overflow-hidden">
          <div className="h-full w-1/2 bg-cyan-500 animate-[shimmer_2s_infinite]" />
        </div>
      </div>
      <h3 className="text-2xl font-black tracking-tight">{value}</h3>
      <p className="text-[10px] font-bold uppercase text-slate-500 mt-1 tracking-widest">{label}</p>
      <p className="text-[8px] text-slate-700 uppercase mt-1">{sub}</p>
    </div>
  );
}

function AutomationCard({ data }) {
  const Icon = data.icon; // Icon Component assignment
  return (
    <div className="p-5 bg-white/[0.01] border border-white/5 rounded-2xl flex items-center justify-between group hover:bg-white/[0.03] hover:border-cyan-400/30 transition-all cursor-pointer">
      <div className="flex items-center gap-4">
        <div className={`p-3 rounded-xl transition-all duration-300 ${data.status === "Active" ? "bg-cyan-500/10 text-cyan-400" : "bg-white/5 text-slate-600"}`}>
          <Icon size={18} />
        </div>
        <div>
          <h4 className="text-xs font-bold uppercase text-slate-200 group-hover:text-white transition-colors">{data.name}</h4>
          <span className={`text-[8px] font-black uppercase tracking-tighter ${data.status === "Active" ? "text-cyan-500" : "text-slate-600"}`}>
            {data.status}
          </span>
        </div>
      </div>
      <div className="text-right">
        <div className="text-[10px] font-mono text-slate-500 group-hover:text-cyan-400 transition-colors">{data.load}</div>
        <div className="h-1 w-12 bg-white/5 rounded-full mt-1">
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: data.load }}
            className="h-full bg-cyan-500 rounded-full" 
          />
        </div>
      </div>
    </div>
  );
}

function ControlToggle({ label, desc, active }) {
  const [isOn, setIsOn] = useState(active);
  return (
    <div onClick={() => setIsOn(!isOn)} className="flex items-center justify-between p-5 bg-white/[0.01] border border-white/5 hover:border-white/10 rounded-2xl cursor-pointer transition-all">
      <div>
        <p className="text-[10px] font-black uppercase text-slate-300">{label}</p>
        <p className="text-[8px] text-slate-600 uppercase mt-0.5">{desc}</p>
      </div>
      <div className={`w-10 h-4 rounded-full relative transition-colors duration-300 ${isOn ? 'bg-cyan-500/30' : 'bg-slate-800'}`}>
        <motion.div 
          animate={{ x: isOn ? 24 : 4 }}
          className={`absolute top-1 h-2 w-2 rounded-full bg-white shadow-[0_0_8px_white]`} 
        />
      </div>
    </div>
  );
}

function SectionHeader({ title, icon: Icon }) {
  return (
    <div className="flex items-center gap-4">
      <Icon size={18} className="text-cyan-400 opacity-60" />
      <h3 className="text-[11px] font-black uppercase tracking-[0.4em] text-slate-500">{title}</h3>
      <div className="h-px flex-1 bg-gradient-to-r from-white/10 to-transparent" />
    </div>
  );
}