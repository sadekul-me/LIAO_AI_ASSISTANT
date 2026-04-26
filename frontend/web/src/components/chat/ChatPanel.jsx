import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Heart } from "lucide-react";

import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

/* CONTEXT */
import { useAI } from "../../context/AIContext";
import useUI from "../../hooks/useUI";
import useVoice from "../../hooks/useVoice";

const ChatPanel = () => {
  const { messages = [], isLoading, isOnline } = useAI();
  const { isMobile, theme } = useUI();
  const { isListening, isSupported } = useVoice();

  const bottomRef = useRef(null);

  /* AUTO SCROLL */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, isLoading]);

  const getStatus = () => {
    if (isListening) return "Listening...";
    if (isLoading) return "Thinking...";
    if (!isOnline) return "Offline";
    return "Online";
  };

  return (
    <section className="
      relative w-full h-full flex flex-col
      overflow-hidden
      bg-gradient-to-b from-[#080E1C] via-[#050914] to-[#03060E]
      border-x border-white/[0.04]
    ">

      {/* 🔥 PREMIUM BACKGROUND DEPTH */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-[20%] left-[10%] w-[50%] h-[50%] bg-cyan-500/[0.04] blur-[140px]" />
        <div className="absolute bottom-[0%] right-[0%] w-[40%] h-[40%] bg-pink-500/[0.03] blur-[120px]" />
      </div>

      {/* 🔹 HEADER */}
      <header className="
        relative z-30 shrink-0
        border-b border-white/[0.04]
        bg-[#050914]/70 backdrop-blur-2xl
        px-4 sm:px-6
        py-3
      ">
        <ChatHeader
          status={getStatus()}
          role="ai"
          online={isOnline}
          theme={theme}
          mic={isSupported}
        />
      </header>

      {/* 🔹 MESSAGE AREA */}
      <main className="
        relative flex-1 min-h-0 overflow-y-auto
        px-4 sm:px-8 lg:px-12
        py-6
      ">

        <AnimatePresence mode="popLayout">

          {/* EMPTY STATE */}
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="min-h-full flex flex-col items-center justify-center text-center"
            >
              <div className="relative mb-10">
                <div className="absolute inset-0 bg-pink-500/10 blur-[60px]" />

                <div className="
                  relative w-20 h-20
                  bg-white/[0.02]
                  border border-white/10
                  flex items-center justify-center
                  backdrop-blur-xl
                ">
                  <Heart
                    size={isMobile ? 28 : 34}
                    className="text-pink-400"
                    fill="currentColor"
                  />
                </div>
              </div>

              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
              >
                <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
                  LIAO{" "}
                  <span className="bg-gradient-to-r from-pink-400 via-white to-cyan-400 bg-clip-text text-transparent">
                    Assistant
                  </span>
                </h2>

                <p className="mt-3 text-slate-500 text-xs tracking-[0.35em] uppercase">
                  System Ready
                </p>
              </motion.div>
            </motion.div>
          )}

          {/* MESSAGES */}
          <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8 pb-14">
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25 }}
              >
                <ChatMessage message={msg} />
              </motion.div>
            ))}
          </div>

        </AnimatePresence>

        <div ref={bottomRef} />
      </main>

      {/* 🔹 INPUT AREA */}
      <footer className="
        relative shrink-0
        border-t border-white/[0.05]
        bg-[#03060E]/90 backdrop-blur-2xl
        px-4 sm:px-6 py-3
      ">
        <div className="max-w-4xl mx-auto">
          <ChatInput />
        </div>
      </footer>

      {/* 🔥 FRAME DETAIL */}
      <div className="pointer-events-none absolute inset-0 border border-white/[0.02]" />

    </section>
  );
};

export default ChatPanel;