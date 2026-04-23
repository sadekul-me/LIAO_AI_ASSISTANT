import { motion } from "framer-motion";
import {
  User,
  Sparkles,
  Heart,
} from "lucide-react";

export default function ChatMessage({
  text,
  isUser,
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.28 }}
      className={`w-full flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`
          flex items-end gap-3
          max-w-[92%] md:max-w-[82%]
          ${isUser ? "flex-row-reverse" : "flex-row"}
        `}
      >
        {/* Avatar */}
        <div
          className={`
            shrink-0 w-11 h-11 rounded-2xl
            flex items-center justify-center relative overflow-hidden
            ${
              isUser
                ? "bg-gradient-to-br from-cyan-500 to-purple-500 shadow-[0_0_20px_rgba(34,211,238,0.25)]"
                : "bg-gradient-to-br from-pink-400 via-purple-500 to-cyan-400 shadow-[0_0_25px_rgba(236,72,153,0.25)]"
            }
          `}
        >
          {isUser ? (
            <User size={18} className="text-white z-10" />
          ) : (
            <>
              {/* Hologram Girl Feel */}
              <div className="absolute inset-0 bg-white/10 animate-pulse" />

              <div className="relative z-10 flex flex-col items-center">
                <div className="w-4 h-4 rounded-full bg-white/90 mb-[2px]" />
                <div className="w-6 h-3 rounded-full bg-white/80" />
              </div>

              <Sparkles
                size={10}
                className="absolute top-1 right-1 text-white/80"
              />

              <Heart
                size={9}
                className="absolute bottom-1 left-1 text-pink-100"
              />
            </>
          )}
        </div>

        {/* Bubble */}
        <div className="flex flex-col">
          <span
            className={`
              text-[11px] mb-1 px-1
              ${
                isUser
                  ? "text-right text-cyan-300"
                  : "text-left text-pink-300"
              }
            `}
          >
            {isUser ? "You" : "Nilima"}
          </span>

          <div
            className={`
              relative px-4 py-3 rounded-3xl text-sm leading-relaxed whitespace-pre-wrap break-words
              backdrop-blur-xl border
              ${
                isUser
                  ? `
                    text-white
                    border-cyan-300/10
                    bg-gradient-to-r from-cyan-500 to-purple-500
                    shadow-[0_0_18px_rgba(34,211,238,0.22)]
                    rounded-br-md
                  `
                  : `
                    text-white
                    border-pink-300/10
                    bg-gradient-to-br from-[#1a1025]/95 to-[#0f172a]/90
                    shadow-[0_0_18px_rgba(236,72,153,0.14)]
                    rounded-bl-md
                  `
              }
            `}
          >
            {!isUser && (
              <div className="absolute top-2 right-2 opacity-40">
                <Sparkles
                  size={12}
                  className="text-pink-300"
                />
              </div>
            )}

            {text}
          </div>
        </div>
      </div>
    </motion.div>
  );
}