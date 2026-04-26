import React from "react";
import {
  Sparkles,
  MoreVertical,
  Phone,
  Video,
  ShieldCheck,
  Zap,
} from "lucide-react";
import { motion } from "framer-motion";

import Avatar from "../ai/Avatar";
import Tooltip from "../ui/Tooltip";

const ChatHeader = ({
  name = "Nilima",
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
        bg-[#080E1C]/80 backdrop-blur-2xl
        border-b border-white/[0.06]
      "
    >

      {/* LEFT SIDE */}
      <div className="flex items-center gap-4 min-w-0">

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

        {/* INFO */}
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h2 className="text-white text-sm sm:text-base font-semibold truncate">
              {name}
            </h2>

            {isOnline && (
              <ShieldCheck size={14} className="text-cyan-400" />
            )}
          </div>

          {/* STATUS */}
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

      {/* RIGHT SIDE */}
      <div className="flex items-center gap-2">

        {/* SECURITY BADGE */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10">
          <Zap size={12} className="text-cyan-400" />
          <span className="text-[10px] text-slate-400 uppercase tracking-wider">
            Secure AI
          </span>
        </div>

        {/* ACTIONS */}
        <div className="flex items-center gap-1 p-1 rounded-xl bg-white/5 border border-white/10">

          {/* CALL */}
          <Tooltip text="Voice Call">
            <button
              onClick={onCall}
              className="
                w-9 h-9 flex items-center justify-center
                rounded-lg hover:bg-white/10
                transition active:scale-95
              "
            >
              <Phone size={16} className="text-slate-300" />
            </button>
          </Tooltip>

          {/* VIDEO */}
          <Tooltip text="Video Call">
            <button
              onClick={onVideo}
              className="
                w-9 h-9 flex items-center justify-center
                rounded-lg hover:bg-white/10
                transition active:scale-95
              "
            >
              <Video size={16} className="text-slate-300" />
            </button>
          </Tooltip>

          {/* MENU */}
          <Tooltip text="More Options">
            <button
              onClick={onMenu}
              className="
                w-9 h-9 flex items-center justify-center
                rounded-lg hover:bg-white/10
                transition active:scale-95
              "
            >
              <MoreVertical size={16} className="text-slate-300" />
            </button>
          </Tooltip>

        </div>

        {/* AI ACTION BUTTON */}
        <button
          onClick={onAIAction}
          className="
            relative w-10 h-10 rounded-xl
            bg-gradient-to-br from-cyan-500 via-blue-500 to-purple-600
            flex items-center justify-center
            shadow-[0_0_25px_rgba(34,211,238,0.25)]
            hover:scale-105 transition
            active:scale-95
          "
        >
          <Sparkles size={16} className="text-white" />
        </button>

      </div>

    </motion.header>
  );
};

export default ChatHeader;