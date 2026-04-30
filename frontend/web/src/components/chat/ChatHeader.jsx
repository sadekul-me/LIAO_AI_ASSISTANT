import React from "react";
import {
  Sparkles,
  MoreVertical,
  Phone,
  Video,
  ShieldCheck,
} from "lucide-react";
import { motion } from "framer-motion";

import Avatar from "../ai/Avatar";

const ChatHeader = ({
  name = "LIAO Assistant",
  status = "Online",
  role = "ai",
  avatar = "",
  onCall,
  onVideo,
  onMenu,
  onAIAction,
}) => {
  const isOnline = status?.toLowerCase() === "online";

  return (
    <motion.header
      initial={{ y: -10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="
        relative flex items-center justify-between
        px-4 sm:px-6 py-3
        bg-[#050914]/70 backdrop-blur-2xl
        border-b border-white/[0.06]
      "
    >
      {/* ================= LEFT ================= */}
      <div className="flex items-center gap-3 min-w-0">

        {/* Avatar */}
        <div className="relative">
          <div className="absolute inset-0 rounded-full bg-cyan-500/20 blur-xl opacity-40" />

          <Avatar
            role={role}
            size="md"
            src={avatar}
            name={name}
            online={isOnline}
            className="relative border border-white/10"
          />
        </div>

        {/* Name + Status */}
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h2 className="text-white text-sm sm:text-base font-semibold truncate">
              {name}
            </h2>

            {isOnline && (
              <ShieldCheck size={14} className="text-cyan-400" />
            )}
          </div>

          <div className="flex items-center gap-2 mt-1">
            <span
              className={`w-2 h-2 rounded-full ${
                isOnline
                  ? "bg-cyan-400 shadow-[0_0_10px_#22d3ee]"
                  : "bg-slate-600"
              }`}
            />
            <span className="text-[10px] uppercase tracking-[0.2em] text-slate-400">
              {isOnline ? "Online" : "Offline"}
            </span>
          </div>
        </div>
      </div>

      {/* ================= RIGHT ================= */}
      <div className="flex items-center gap-2">

        {/* CALL / VIDEO GROUP (NO BORDER BOX → CLEAN PREMIUM) */}
        <div className="flex items-center gap-1">

          {/* CALL */}
          <button
            onClick={onCall}
            className="
              w-9 h-9 flex items-center justify-center
              rounded-lg
              hover:bg-white/10
              transition active:scale-95
              group
            "
          >
            <Phone
              size={16}
              className="text-slate-300 group-hover:text-cyan-300 transition"
            />
          </button>

          {/* VIDEO */}
          <button
            onClick={onVideo}
            className="
              w-9 h-9 flex items-center justify-center
              rounded-lg
              hover:bg-white/10
              transition active:scale-95
              group
            "
          >
            <Video
              size={16}
              className="text-slate-300 group-hover:text-cyan-300 transition"
            />
          </button>

          {/* MENU */}
          <button
            onClick={onMenu}
            className="
              w-9 h-9 flex items-center justify-center
              rounded-lg
              hover:bg-white/10
              transition active:scale-95
              group
            "
          >
            <MoreVertical
              size={16}
              className="text-slate-300 group-hover:text-white transition"
            />
          </button>
        </div>

        {/* AI BUTTON (MAIN FOCUS GLOW) */}
        <button
          onClick={onAIAction}
          className="
            relative w-10 h-10 rounded-xl
            bg-gradient-to-br from-cyan-500 via-blue-500 to-purple-600
            flex items-center justify-center
            shadow-[0_0_25px_rgba(34,211,238,0.25)]
            hover:scale-105 transition active:scale-95
          "
        >
          <Sparkles size={16} className="text-white" />
        </button>

      </div>
    </motion.header>
  );
};

export default ChatHeader;