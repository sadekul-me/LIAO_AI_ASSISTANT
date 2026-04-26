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
    /* ✅ ROOT FIX: NO 100vh HERE */
    <section className="
      relative w-full h-full flex flex-col
      overflow-hidden
      bg-gradient-to-b from-[#080E1C] via-[#050914] to-[#03060E]
      border-x sm:border border-white/[0.05]
      sm:rounded-[30px]
    ">

      {/* BACKGROUND GLOW */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-[10%] -left-[10%] w-[60%] h-[60%] bg-cyan-500/[0.03] blur-[120px] rounded-full" />
        <div className="absolute top-[20%] -right-[10%] w-[40%] h-[40%] bg-pink-500/[0.03] blur-[100px] rounded-full" />
      </div>

      {/* HEADER (FIXED - NEVER CUT) */}
      <header className="
        shrink-0 z-30
        border-b border-white/[0.04]
        bg-[#080E1C]/60 backdrop-blur-xl
      ">
        <ChatHeader
          status={getStatus()}
          role="ai"
          online={isOnline}
          theme={theme}
          mic={isSupported}
        />
      </header>

      {/* MESSAGES AREA (ONLY SCROLLABLE PART) */}
      <main className="
        flex-1 min-h-0 overflow-y-auto
        px-4 sm:px-8 lg:px-10
        py-5 sm:py-6
      ">
        <AnimatePresence mode="popLayout">

          {/* EMPTY STATE */}
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="min-h-full flex flex-col items-center justify-center text-center px-4"
            >
              <div className="relative mb-8">
                <div className="absolute inset-0 bg-pink-500/20 blur-[50px] animate-pulse rounded-full" />

                <div className="
                  relative w-20 h-20 sm:w-24 sm:h-24
                  rounded-[2rem]
                  bg-white/[0.03]
                  border border-white/10
                  flex items-center justify-center
                  backdrop-blur-2xl
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
                <h2 className="text-2xl sm:text-4xl font-black text-white">
                  LIAO{" "}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 via-white to-cyan-400 italic">
                    Assistant
                  </span>
                </h2>

                <p className="mt-2 text-slate-500 text-xs sm:text-sm tracking-[0.3em] uppercase">
                  Ready when you are
                </p>
              </motion.div>
            </motion.div>
          )}

          {/* MESSAGES */}
          <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8 pb-10">
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <ChatMessage message={msg} />
              </motion.div>
            ))}
          </div>

        </AnimatePresence>

        <div ref={bottomRef} />
      </main>

      {/* INPUT (FIXED - NO ABSOLUTE) */}
      <footer className="
        shrink-0
        border-t border-white/[0.05]
        bg-[#03060E]/80 backdrop-blur-xl
        p-3 sm:p-4
      ">
        <div className="max-w-4xl mx-auto">
          <ChatInput />
        </div>
      </footer>

    </section>
  );
};

export default ChatPanel;