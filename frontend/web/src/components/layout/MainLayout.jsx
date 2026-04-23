import { useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import ChatPanel from "../chat/ChatPanel";
import Dashboard from "../../pages/Dashboard";
import SettingsPanel from "../settings/SettingsPanel";

export default function MainLayout() {
  const [openSettings, setOpenSettings] = useState(false);

  return (
    <div className="h-screen w-full bg-[#0B0F19] text-white relative overflow-hidden">

      {/* 🌌 BACKGROUND */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute w-[700px] h-[700px] bg-cyan-500/10 blur-[200px] top-[-250px] left-[5%]" />
        <div className="absolute w-[600px] h-[600px] bg-purple-500/10 blur-[200px] bottom-[-200px] right-[5%]" />
      </div>

      <div className="absolute inset-0 bg-gradient-to-br from-[#0B0F19] via-[#0B0F19] to-black opacity-90 pointer-events-none" />

      {/* 🧠 TOPBAR */}
      <Topbar onOpenSettings={() => setOpenSettings(true)} />

      {/* 📦 MAIN */}
      <div className="flex h-full pt-16">
        <Sidebar />

        <div className="flex-1 flex items-center justify-center">
          <Dashboard />
        </div>

        <ChatPanel />
      </div>

      {/* ⚙️ SETTINGS PANEL */}
      <SettingsPanel
        isOpen={openSettings}
        onClose={() => setOpenSettings(false)}
      />

    </div>
  );
}