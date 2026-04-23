import React from "react";
import { motion } from "framer-motion";
import {
  Mic,
  Heart,
  Sparkles,
  Activity,
} from "lucide-react";

import Orb from "../components/ui/Orb";

export default function Dashboard() {
  return (
    <div className="relative w-full h-screen overflow-hidden bg-[#04060a] text-white">

      {/* ===== SOFT BACKGROUND LAYERS ===== */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[60%] h-[60%] bg-cyan-500/10 blur-[180px] rounded-full" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[60%] h-[60%] bg-purple-500/10 blur-[180px] rounded-full" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.04),transparent_60%)]" />
      </div>

      {/* ===== MAIN WRAPPER ===== */}
      <div className="relative z-10 h-full flex flex-col px-6 md:px-12 py-8">

        {/* ===== CENTER SECTION ===== */}
        <div className="flex-1 flex items-center justify-center">

          <div className="grid lg:grid-cols-2 gap-14 items-center w-full max-w-6xl">

            {/* LEFT CONTENT */}
            <div className="space-y-6 text-center lg:text-left">

              {/* STATUS BADGE */}
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-xl">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                <p className="text-[11px] tracking-[0.25em] text-gray-300 uppercase">
                  Emotional AI Active
                </p>
              </div>

              {/* TITLE */}
              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                NILIMA
                <span className="block bg-gradient-to-r from-cyan-300 via-white to-purple-400 bg-clip-text text-transparent">
                  COMPANION
                </span>
              </h1>

              {/* DESCRIPTION */}
              <p className="text-gray-400 text-sm max-w-md leading-relaxed">
                A living emotional AI presence designed to listen, respond and stay with you like a real companion.
              </p>

              {/* MIC CARD */}
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="flex items-center gap-4 p-5 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl w-fit shadow-[0_0_40px_rgba(34,211,238,0.05)]"
              >
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-r from-cyan-500/20 to-purple-500/20 flex items-center justify-center">
                  <Mic className="text-cyan-300" />
                </div>

                <div>
                  <p className="text-sm font-semibold">Voice Presence</p>
                  <p className="text-xs text-gray-400">Listening with emotional awareness</p>
                </div>
              </motion.div>

            </div>

            {/* RIGHT ORB (CENTER FEEL) */}
            <div className="flex items-center justify-center relative">

              {/* glow ring */}
              <div className="absolute w-[420px] h-[420px] bg-cyan-500/10 blur-[120px] rounded-full" />

              <Orb />

            </div>

          </div>
        </div>

        {/* ===== FLOATING BOTTOM DOCK (FIXED + PREMIUM) ===== */}
        <div className="h-[140px] flex items-center justify-center">
          <div className="grid grid-cols-3 gap-4 w-full max-w-4xl">

            <Card icon={<Heart />} title="Bond" value="Emotional" />
            <Card icon={<Sparkles />} title="Intelligence" value="Adaptive" />
            <Card icon={<Activity />} title="System" value="Alive" />

          </div>
        </div>

      </div>
    </div>
  );
}

/* ===== PREMIUM CARD ===== */
function Card({ icon, title, value }) {
  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.02 }}
      className="
        relative
        p-5 rounded-3xl
        border border-white/10
        bg-white/5
        backdrop-blur-xl
        flex items-center gap-4
        h-[92px]
        overflow-hidden
      "
    >
      {/* glow overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 to-purple-500/5 opacity-0 hover:opacity-100 transition" />

      <div className="w-11 h-11 rounded-2xl bg-white/5 flex items-center justify-center text-cyan-300">
        {React.cloneElement(icon, { size: 18 })}
      </div>

      <div>
        <p className="text-[10px] text-gray-400 uppercase tracking-[0.25em]">
          {title}
        </p>
        <p className="text-sm font-semibold text-white">
          {value}
        </p>
      </div>
    </motion.div>
  );
}