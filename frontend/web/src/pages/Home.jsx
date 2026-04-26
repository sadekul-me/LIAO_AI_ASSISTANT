import React from "react";
import ChatPanel from "../components/chat/ChatPanel";
import RightPanel from "../components/layout/RightPanel";

/**
 * Home Component
 * Main layout (Chat + Right Panel)
 */
const Home = () => {
  return (
    <main className="h-screen w-full bg-[#02040D] p-2 md:p-3 lg:p-4">
      
      {/* MAIN WRAPPER */}
      <div className="flex h-full w-full gap-2.5 rounded-2xl lg:gap-3 overflow-hidden">

        {/* LEFT: CHAT PANEL */}
        <section className="flex-1 min-w-0 h-full rounded-2xl bg-[#0A0C16]/50 shadow-[0_18px_70px_rgba(0,0,0,0.55)] overflow-hidden">
          <ChatPanel />
        </section>

        {/* RIGHT: DASHBOARD PANEL */}
        <aside className="hidden xl:flex xl:w-[310px] 2xl:w-[350px] h-full rounded-2xl bg-[#0A0C16]/50 shadow-[0_18px_70px_rgba(0,0,0,0.55)] overflow-hidden">
          <RightPanel />
        </aside>

      </div>
    </main>
  );
};

export default Home;