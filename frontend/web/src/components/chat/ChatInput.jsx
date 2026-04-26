import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Mic, Heart, Sparkles, Smile } from "lucide-react";
import { useAI } from "../../context/AIContext";

export default function ChatInput() {
  const { sendMessage, isLoading, isListening, toggleListening } = useAI();

  const [message, setMessage] = useState("");
  const textareaRef = useRef(null);

  /* =========================
     AUTO RESIZE
  ========================= */
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;

    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 140) + "px";
  }, [message]);

  /* =========================
     SEND
  ========================= */
  const handleSend = async () => {
    const text = message.trim();
    if (!text || isLoading) return;

    setMessage("");
    await sendMessage(text);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const sendLove = async () => {
    if (isLoading) return;
    await sendMessage("Are you with me today? 💖");
  };

  return (
    <div className="w-full px-3 sm:px-4">

      {/* WRAPPER */}
      <div
        className="
          relative flex items-center gap-2
          rounded-[26px]
          border border-white/[0.08]
          bg-white/[0.04]
          backdrop-blur-2xl
          shadow-[0_10px_40px_rgba(0,0,0,0.25)]
          px-2 py-2
          overflow-hidden
        "
      >

        {/* TOP GLOW */}
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent" />

        {/* MIC */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={toggleListening}
          disabled={isLoading}
          className={`
            w-11 h-11 shrink-0
            rounded-2xl
            flex items-center justify-center
            transition
            ${
              isListening
                ? "bg-gradient-to-r from-pink-500 to-purple-500 shadow-[0_0_25px_rgba(236,72,153,0.35)]"
                : "bg-white/[0.05] hover:bg-white/[0.1]"
            }
          `}
        >
          <Mic size={18} className="text-white" />
        </motion.button>

        {/* INPUT */}
        <div className="flex-1 flex items-center min-w-0">

          {/* emoji */}
          <Smile
            size={16}
            className="text-slate-500 hidden sm:block shrink-0"
          />

          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            rows={1}
            placeholder={
              isLoading
                ? "Thinking..."
                : isListening
                ? "Listening..."
                : "Ask anything..."
            }
            className="
              flex-1 bg-transparent outline-none resize-none
              text-sm sm:text-[15px]
              text-white placeholder:text-slate-500
              leading-relaxed
              max-h-[140px]
              px-2
              overflow-y-auto
            "
          />

          <Sparkles
            size={14}
            className="text-cyan-300/70 shrink-0"
          />
        </div>

        {/* LOVE */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={sendLove}
          disabled={isLoading}
          className="
            hidden sm:flex shrink-0
            w-10 h-10
            rounded-2xl
            items-center justify-center
            bg-white/[0.05] hover:bg-white/[0.1]
            transition
          "
        >
          <Heart size={16} className="text-pink-300" />
        </motion.button>

        {/* SEND */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={handleSend}
          disabled={isLoading || !message.trim()}
          className={`
            w-11 h-11 shrink-0
            rounded-2xl
            flex items-center justify-center
            transition
            ${
              isLoading || !message.trim()
                ? "bg-white/[0.06] opacity-50"
                : "bg-gradient-to-r from-cyan-500 to-purple-500 shadow-[0_0_25px_rgba(34,211,238,0.25)] hover:shadow-[0_0_35px_rgba(168,85,247,0.35)]"
            }
          `}
        >
          <Send size={18} className="text-white" />
        </motion.button>

      </div>
    </div>
  );
}