import { useState } from "react";
import { motion } from "framer-motion";
import {
  Send,
  Mic,
  Heart,
  Sparkles,
  Smile,
} from "lucide-react";

export default function ChatInput({
  onSend,
}) {
  const [message, setMessage] = useState("");
  const [isListening, setIsListening] = useState(false);

  /* SEND */
  const handleSend = () => {
    const text = message.trim();

    if (!text) return;

    onSend?.(text);
    setMessage("");
  };

  /* ENTER SEND */
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /* MIC */
  const toggleMic = () => {
    setIsListening((prev) => !prev);
  };

  /* QUICK LOVE */
  const sendLove = () => {
    onSend?.("Nilima, tumi amar sathe acho? 💖");
  };

  return (
    <div
      className="
        px-4 py-3
        border-t border-white/10
        bg-[#08111f]/90
        backdrop-blur-3xl
        relative
      "
    >
      {/* top glow */}
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-400/30 to-transparent" />

      {/* MAIN BAR */}
      <div
        className="
          flex items-center gap-2
          rounded-[28px]
          px-3 py-2
          border border-white/10
          bg-white/[0.04]
          shadow-[0_0_25px_rgba(0,255,255,0.04)]
        "
      >
        {/* MIC */}
        <motion.button
          whileTap={{ scale: 0.92 }}
          onClick={toggleMic}
          className={`
            relative
            w-11 h-11 rounded-2xl
            flex items-center justify-center
            transition-all duration-300
            ${
              isListening
                ? "bg-gradient-to-r from-pink-500 to-purple-500 shadow-[0_0_20px_rgba(236,72,153,0.35)]"
                : "bg-white/[0.05] hover:bg-white/[0.09]"
            }
          `}
        >
          <Mic size={18} className="text-white" />

          {isListening && (
            <span className="absolute inset-0 rounded-2xl border border-pink-300/40 animate-ping" />
          )}
        </motion.button>

        {/* INPUT */}
        <div className="flex-1 flex items-center gap-2 px-1">
          <Smile
            size={18}
            className="text-gray-400 hidden sm:block"
          />

          <input
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Message Nilima..."
            className="
              w-full bg-transparent outline-none
              text-sm text-white
              placeholder:text-gray-400
            "
          />

          <Sparkles
            size={15}
            className="text-cyan-300/70"
          />
        </div>

        {/* LOVE */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={sendLove}
          className="
            hidden sm:flex
            w-10 h-10 rounded-2xl
            items-center justify-center
            bg-white/[0.05]
            hover:bg-white/[0.09]
            transition
          "
        >
          <Heart
            size={16}
            className="text-pink-300"
          />
        </motion.button>

        {/* SEND */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={handleSend}
          className="
            w-11 h-11 rounded-2xl
            flex items-center justify-center
            bg-gradient-to-r from-cyan-500 to-purple-500
            hover:scale-[1.03]
            shadow-[0_0_18px_rgba(34,211,238,0.28)]
            hover:shadow-[0_0_28px_rgba(168,85,247,0.38)]
            transition-all
          "
        >
          <Send
            size={18}
            className="text-white"
          />
        </motion.button>
      </div>

      {/* STATUS */}
      <div className="px-2 pt-2 min-h-[18px]">
        {isListening ? (
          <p className="text-[11px] text-pink-300 animate-pulse">
            🎙 Nilima is listening...
          </p>
        ) : (
          <p className="text-[11px] text-gray-500">
            Nilima is online • Ready to reply
          </p>
        )}
      </div>
    </div>
  );
}