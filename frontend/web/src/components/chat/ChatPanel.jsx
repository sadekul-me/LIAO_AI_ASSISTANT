import {
  motion,
  AnimatePresence,
} from "framer-motion";
import {
  MessageCircle,
  Sparkles,
  Bot,
  Trash2,
} from "lucide-react";

import {
  useEffect,
  useRef,
} from "react";

import useAI from "../../hooks/useAI";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

export default function ChatPanel() {
  const {
    messages,
    sendMessage,
    isLoading,
    clearChat,
  } = useAI();

  const chatRef = useRef(null);
  const bottomRef = useRef(null);

  /* AUTO SCROLL TO LAST MESSAGE */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, isLoading]);

  return (
    <div
      className="
        w-full md:w-[430px] xl:w-[450px]
        h-full
        flex flex-col
        border-l border-white/10
        bg-[#08111f]/75
        backdrop-blur-3xl
        overflow-hidden
        relative
      "
    >
      {/* BACKGROUND GLOW */}
      <div className="absolute top-10 right-10 w-32 h-32 bg-cyan-500/10 blur-3xl rounded-full pointer-events-none" />
      <div className="absolute bottom-20 left-6 w-32 h-32 bg-purple-500/10 blur-3xl rounded-full pointer-events-none" />

      {/* HEADER */}
      <div
        className="
          relative z-10
          px-5 py-4
          border-b border-white/10
          flex items-center justify-between
          bg-white/[0.03]
          backdrop-blur-2xl
        "
      >
        <div className="flex items-center gap-3 min-w-0">
          {/* AVATAR */}
          <div
            className="
              w-11 h-11 rounded-2xl
              bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-500
              flex items-center justify-center
              shadow-[0_0_25px_rgba(34,211,238,0.25)]
            "
          >
            <Bot
              size={19}
              className="text-white"
            />
          </div>

          {/* TITLE */}
          <div className="min-w-0">
            <h2 className="text-white text-sm font-semibold">
              Nilima Chat
            </h2>

            <div className="flex items-center gap-2 mt-0.5">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />

              <p className="text-[11px] text-gray-400 truncate">
                Online • Instant Reply
              </p>
            </div>
          </div>
        </div>

        {/* CLEAR BTN */}
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={clearChat}
          className="
            w-10 h-10 rounded-2xl
            flex items-center justify-center
            bg-white/[0.04]
            hover:bg-white/[0.08]
            border border-white/10
            transition
          "
        >
          <Trash2
            size={16}
            className="text-gray-300"
          />
        </motion.button>
      </div>

      {/* CHAT BODY */}
      <div
        ref={chatRef}
        className="
          relative z-10
          flex-1
          overflow-y-auto
          px-4 py-4
          space-y-4
          scroll-smooth
          custom-scrollbar
        "
      >
        {/* EMPTY STATE */}
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center text-gray-400 px-6">
            <div
              className="
                w-16 h-16 rounded-3xl
                bg-white/[0.04]
                border border-white/10
                flex items-center justify-center
                mb-4
              "
            >
              <MessageCircle
                size={26}
                className="opacity-70"
              />
            </div>

            <p className="text-sm text-white">
              Start chatting with Nilima
            </p>

            <p className="text-xs mt-2 text-gray-500 max-w-[220px] leading-relaxed">
              Warm, natural and premium conversation experience.
            </p>
          </div>
        )}

        {/* MESSAGES */}
        <AnimatePresence initial={false}>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{
                opacity: 0,
                y: 14,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              exit={{ opacity: 0 }}
              transition={{
                duration: 0.22,
              }}
            >
              <ChatMessage
                text={msg.text}
                isUser={msg.isUser}
              />
            </motion.div>
          ))}
        </AnimatePresence>

        {/* THINKING */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="
              flex items-center gap-3
              px-4 py-3
              rounded-2xl
              bg-white/[0.04]
              border border-white/10
              max-w-[85%]
              backdrop-blur-xl
            "
          >
            <Sparkles
              size={16}
              className="text-cyan-300 animate-pulse"
            />

            <span className="text-sm text-gray-300">
              Nilima is thinking...
            </span>
          </motion.div>
        )}

        {/* AUTO SCROLL TARGET */}
        <div ref={bottomRef} />
      </div>

      {/* INPUT */}
      <div
        className="
          relative z-10
          border-t border-white/10
          bg-white/[0.02]
          backdrop-blur-2xl
        "
      >
        <ChatInput onSend={sendMessage} />
      </div>
    </div>
  );
}