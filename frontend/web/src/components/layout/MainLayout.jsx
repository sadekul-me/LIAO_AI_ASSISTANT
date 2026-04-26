import React, { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

import Sidebar from "./Sidebar";
import RightPanel from "./RightPanel";

import Dashboard from "../../pages/Dashboard";
import ChatPanel from "../chat/ChatPanel";
import SettingsPanel from "../settings/SettingsPanel";
import AutomationEngine from "../settings/AutomationEngine";

const PAGE_MAP = {
  dashboard: Dashboard,
  chat: ChatPanel,
  // সেটিংসকে আমরা ম্যাপে রাখব না কারণ এটা ওভারলে হিসেবে কাজ করে
  automation: AutomationEngine 
};

const MainLayout = () => {
  // শুরুতে ড্যাশবোর্ড অ্যাক্টিভ থাকবে
  const [activePage, setActivePage] = useState("dashboard");
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  const ActiveComponent = useMemo(() => {
    // যদি সেটিংস ওপেন না থাকে এবং পেজ ম্যাপে থাকে তবেই কম্পোনেন্ট রিটার্ন করবে
    return PAGE_MAP[activePage] || Dashboard;
  }, [activePage]);

  // 🔥 নেভিগেশন হ্যান্ডলার: সেটিংস এবং অটোমেশন লজিক আলাদা করা হয়েছে
  const handleNavClick = (page) => {
    if (page === "settings") {
      setIsSettingsOpen(true);
      setActivePage("settings"); 
    } else {
      // অন্য কোনো পেজে (যেমন: Automation) ক্লিক করলে সেটিংস প্যানেল বন্ধ হয়ে যাবে
      setIsSettingsOpen(false); 
      setActivePage(page);
    }
  };

  return (
    <div className="relative flex h-screen w-full bg-[#02040A] text-white overflow-hidden font-sans">
      
      {/* 🌌 Background Engine */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.015]" />
        {/* Lì Ào Protocol Ambient Glow */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyan-500/5 blur-[120px] rounded-full opacity-20" />
      </div>

      {/* 🔹 Sidebar - High Priority Z-Index */}
      <div className="z-[60] relative">
        <Sidebar active={activePage} setActive={handleNavClick} />
      </div>

      {/* 🔹 Center Content Area */}
      <main className="relative flex-1 flex flex-col min-w-0 z-10 overflow-hidden border-x border-white/[0.03]">

        <AnimatePresence mode="wait">
          {/* যদি সেটিংস ওভারলে ওপেন না থাকে, তবেই পেজ ট্রানজিশন হবে */}
          {!isSettingsOpen && (
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3, ease: "circOut" }}
              className="h-full w-full"
            >
              <ActiveComponent />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ⚙️ Settings Overlay - এটা মেইন কন্টেন্টের উপরে ভেসে থাকবে */}
        <SettingsPanel 
          isOpen={isSettingsOpen} 
          onClearChat={() => console.log("Lì Ào Protocol: Chat History Purged")}
        />

      </main>

      {/* 🔹 Right Panel - System Metrics & Activity */}
      <aside className="hidden lg:block w-[300px] xl:w-[320px] h-full z-10">
        <RightPanel activePage={activePage} />
      </aside>

      {/* Global Interface Border */}
      <div className="fixed inset-0 border border-white/[0.02] pointer-events-none z-50" />
    </div>
  );
};

export default MainLayout;