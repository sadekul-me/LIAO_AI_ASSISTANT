import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Search, FileText, Globe, Folder, 
  Filter, ArrowRight, Clock, HardDrive, 
  FileCode, Image as ImageIcon, Music, Video,
  X, Zap
} from "lucide-react";

export default function FileSearch() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [searchType, setSearchType] = useState("local"); // local or web

  const recentFiles = [
    { name: "LiaoEngine_Core.cs", type: "code", size: "12 KB", date: "2 mins ago" },
    { name: "SystemArchitecture_v3.pdf", type: "document", size: "4.5 MB", date: "1 hour ago" },
    { name: "Dashboard_Preview.png", type: "image", size: "2.1 MB", date: "Yesterday" },
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    if (!searchQuery) return;
    setIsSearching(true);
    // ব্যাকএন্ড এপিআই কল করার সিমুলেশন
    setTimeout(() => setIsSearching(false), 1500);
  };

  return (
    <div className="h-full w-full bg-[#02040A]/50 text-white p-6 lg:p-8 flex flex-col gap-8 overflow-hidden backdrop-blur-xl border border-white/5 rounded-[40px] relative">
      
      {/* 🔮 NEURAL GLOW EFFECTS */}
      <div className="absolute -top-24 -right-24 w-64 h-64 bg-cyan-500/10 blur-[100px] rounded-full pointer-events-none" />
      <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-blue-500/10 blur-[100px] rounded-full pointer-events-none" />

      {/* 🚀 SEARCH HEADER */}
      <div className="relative z-10 flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xs font-black uppercase tracking-[0.4em] text-slate-500">Universal Indexer</h2>
            <p className="text-[10px] text-cyan-400/60 font-mono mt-1">SADIK_NODE // FILE_SEARCH_READY</p>
          </div>
          <div className="flex gap-2 bg-white/5 p-1 rounded-xl border border-white/5">
            <button 
              onClick={() => setSearchType("local")}
              className={`px-4 py-1.5 rounded-lg text-[9px] font-bold uppercase transition-all ${searchType === 'local' ? 'bg-cyan-500 text-black shadow-lg shadow-cyan-500/20' : 'text-slate-500 hover:text-slate-300'}`}
            >
              Local
            </button>
            <button 
              onClick={() => setSearchType("web")}
              className={`px-4 py-1.5 rounded-lg text-[9px] font-bold uppercase transition-all ${searchType === 'web' ? 'bg-purple-500 text-white shadow-lg shadow-purple-500/20' : 'text-slate-500 hover:text-slate-300'}`}
            >
              Neural Web
            </button>
          </div>
        </div>

        {/* 🔍 MAIN SEARCH BAR */}
        <form onSubmit={handleSearch} className="relative group">
          <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none">
            {searchType === "local" ? (
              <Search size={18} className="text-slate-500 group-focus-within:text-cyan-400 transition-colors" />
            ) : (
              <Globe size={18} className="text-slate-500 group-focus-within:text-purple-400 transition-colors" />
            )}
          </div>
          <input 
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={searchType === "local" ? "Search local files, folders, code..." : "Ask Lì Ào anything on the web..."}
            className="w-full bg-white/[0.03] border border-white/10 rounded-2xl py-5 pl-14 pr-24 outline-none focus:border-white/20 focus:bg-white/[0.05] transition-all text-sm font-mono placeholder:text-slate-700"
          />
          <div className="absolute inset-y-2.5 right-2.5 flex gap-2">
            {searchQuery && (
              <button 
                type="button"
                onClick={() => setSearchQuery("")}
                className="p-2 hover:bg-white/10 rounded-xl text-slate-500 transition-colors"
              >
                <X size={16} />
              </button>
            )}
            <button 
              type="submit"
              className={`px-6 rounded-xl font-black text-[10px] uppercase tracking-widest flex items-center gap-2 transition-all ${
                searchType === 'local' ? 'bg-cyan-500 text-black' : 'bg-purple-600 text-white'
              }`}
            >
              {isSearching ? <Zap size={14} className="animate-spin" /> : "Scan"}
            </button>
          </div>
        </form>
      </div>

      {/* 📂 QUICK ACCESS & RESULTS */}
      <div className="relative z-10 flex-1 flex flex-col gap-6 overflow-hidden">
        <div className="flex items-center gap-4">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
            <Clock size={12} /> Recent System Activity
          </span>
          <div className="h-px flex-1 bg-gradient-to-r from-white/10 to-transparent" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 overflow-y-auto pr-2 custom-scrollbar">
          {recentFiles.map((file, idx) => (
            <FileItem key={idx} file={file} />
          ))}
          
          {/* QUICK CATEGORIES */}
          <div className="md:col-span-2 lg:col-span-3 grid grid-cols-2 md:grid-cols-4 gap-4 mt-2">
            <CategoryCard icon={FileCode} label="Codebase" count="1.2k" color="text-emerald-400" />
            <CategoryCard icon={ImageIcon} label="Assets" count="842" color="text-amber-400" />
            <CategoryCard icon={HardDrive} label="Drives" count="3" color="text-cyan-400" />
            <CategoryCard icon={Filter} label="Advanced" count="Logic" color="text-purple-400" />
          </div>
        </div>
      </div>

      {/* 📊 FOOTER STATUS */}
      <div className="relative z-10 border-t border-white/5 pt-4 flex justify-between items-center opacity-40">
        <div className="flex gap-4 text-[9px] font-mono uppercase tracking-tighter">
          <span>Indexer: v3.0.2</span>
          <span>Status: Synchronized</span>
        </div>
        <div className="text-[9px] font-mono text-cyan-500">
          LÌ ÀO PROTOCOL ENCRYPTED
        </div>
      </div>
    </div>
  );
}

// --- Internal Specialized Components ---

function FileItem({ file }) {
  const getIcon = (type) => {
    switch (type) {
      case 'code': return <FileCode size={18} className="text-emerald-400" />;
      case 'image': return <ImageIcon size={18} className="text-amber-400" />;
      default: return <FileText size={18} className="text-cyan-400" />;
    }
  };

  return (
    <motion.div 
      whileHover={{ y: -2, backgroundColor: "rgba(255, 255, 255, 0.04)" }}
      className="p-4 bg-white/[0.02] border border-white/5 rounded-2xl flex items-center gap-4 cursor-pointer transition-all"
    >
      <div className="p-3 bg-white/5 rounded-xl">
        {getIcon(file.type)}
      </div>
      <div className="flex-1 overflow-hidden">
        <h4 className="text-xs font-bold truncate text-slate-200">{file.name}</h4>
        <div className="flex items-center gap-2 mt-1">
          <span className="text-[8px] font-black uppercase text-slate-500">{file.size}</span>
          <div className="h-1 w-1 rounded-full bg-slate-700" />
          <span className="text-[8px] font-medium text-slate-600">{file.date}</span>
        </div>
      </div>
      <ArrowRight size={14} className="text-slate-700 opacity-0 group-hover:opacity-100 transition-opacity" />
    </motion.div>
  );
}

function CategoryCard({ icon: Icon, label, count, color }) {
  return (
    <div className="p-4 bg-white/[0.01] border border-white/5 rounded-2xl hover:border-white/10 transition-all flex items-center justify-between group">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg bg-white/5 ${color} group-hover:scale-110 transition-transform`}>
          <Icon size={14} />
        </div>
        <span className="text-[9px] font-black uppercase tracking-widest text-slate-400">{label}</span>
      </div>
      <span className="text-[10px] font-mono text-slate-600">{count}</span>
    </div>
  );
}