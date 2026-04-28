import React, { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

// Layout Components
import Sidebar from "./Sidebar";
import RightPanel from "./RightPanel";

// Page / Feature Components
import Dashboard from "../../pages/Dashboard";
import ChatPanel from "../chat/ChatPanel";
import SettingsPanel from "../settings/SettingsPanel";
import AutomationEngine from "../settings/AutomationEngine";
import CodeAssistant from "../chat/CodeAssistant";
import SystemControl from "../dashboard/SystemControl";
import FileSearch from "../dashboard/FileSearch";
import ToolBox from "../dashboard/ToolBox";
import VoiceAvatar from "../voice/VoiceAvatar";

const PAGE_MAP = {
  dashboard: Dashboard,
  chat: ChatPanel,
  voice: VoiceAvatar, // ✅ Added
  code: CodeAssistant,
  system: SystemControl,
  files: FileSearch,
  automation: AutomationEngine,
  tools: ToolBox,
  settings: SettingsPanel,
};

const MainLayout = () => {
  const [activePage, setActivePage] = useState("dashboard");

  const ActiveComponent = useMemo(() => {
    return PAGE_MAP[activePage] || Dashboard;
  }, [activePage]);

  const handleNavClick = (page) => {
    setActivePage(page);
  };

  return (
    <div className="relative flex h-screen w-screen overflow-hidden bg-[#02040A] text-white font-sans selection:bg-cyan-500/30">
      
      {/* 🌌 Background */}
      <div className="absolute inset-0 z-0 pointer-events-none select-none overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.015]" />
        <div className="absolute top-0 right-0 h-[600px] w-[600px] rounded-full bg-cyan-500/5 blur-[120px] animate-pulse" />
        <div className="absolute bottom-0 left-0 h-[400px] w-[400px] rounded-full bg-blue-500/5 blur-[120px]" />
      </div>

      {/* 🛰 Sidebar */}
      <aside className="relative z-50 h-full shrink-0 border-r border-white/[0.04] bg-[#02040A]/40 backdrop-blur-3xl">
        <Sidebar active={activePage} setActive={handleNavClick} />
      </aside>

      {/* 🖥 Main Content */}
      <main className="relative z-10 flex h-full min-w-0 flex-1 flex-col overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={activePage}
            initial={{ opacity: 0, x: 20, scale: 0.985 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: -20, scale: 0.985 }}
            transition={{
              duration: 0.28,
              ease: [0.22, 1, 0.36, 1],
            }}
            className="h-full w-full flex-1 overflow-hidden"
          >
            <div className="h-full w-full overflow-hidden">
              <ActiveComponent
                onClearChat={() => console.log("Memory Purged")}
              />
            </div>
          </motion.div>
        </AnimatePresence>
      </main>

      {/* 📊 Right Panel */}
      <aside className="relative z-40 hidden h-full w-[340px] shrink-0 overflow-hidden border-l border-white/[0.04] bg-[#02040A]/20 backdrop-blur-3xl xl:flex">
        <RightPanel activePage={activePage} />
      </aside>

      {/* 🛡 Global Frame */}
      <div className="pointer-events-none fixed inset-0 z-[1000] rounded-sm border border-white/[0.02]" />
    </div>
  );
};

export default MainLayout;