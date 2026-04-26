import { motion } from "framer-motion";
import {
  User,
  Sparkles,
  Bot,
  Copy,
  Check,
} from "lucide-react";
import { useState } from "react";

export default function ChatMessage({
  message,
}) {
  const [copied, setCopied] =
    useState(false);

  /* =========================================
     SAFE DATA HANDLING (IMPORTANT FIX)
  ========================================= */
  const text =
    message?.content ||
    message?.text ||
    "";

  const isUser =
    message?.role === "user" ||
    message?.isUser === true;

  const time =
    message?.time || "";

  /* =========================================
     COPY TEXT
  ========================================= */
  const copyMessage =
    async () => {
      try {
        await navigator.clipboard.writeText(
          text
        );

        setCopied(true);

        setTimeout(() => {
          setCopied(false);
        }, 1500);
      } catch (err) {
        console.warn(
          "Copy failed",
          err
        );
      }
    };

  return (
    <motion.div
      initial={{
        opacity: 0,
        y: 16,
        scale: 0.98,
      }}
      animate={{
        opacity: 1,
        y: 0,
        scale: 1,
      }}
      transition={{
        duration: 0.28,
      }}
      className={`w-full flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`
          flex items-end gap-3
          max-w-[96%] sm:max-w-[90%] lg:max-w-[80%]
          ${
            isUser
              ? "flex-row-reverse"
              : "flex-row"
          }
        `}
      >
        {/* AVATAR */}
        <div
          className={`
            shrink-0
            w-10 h-10 sm:w-11 sm:h-11
            rounded-2xl
            flex items-center justify-center
            relative overflow-hidden
            ${
              isUser
                ? "bg-gradient-to-br from-cyan-500 to-purple-500 shadow-[0_0_20px_rgba(34,211,238,0.25)]"
                : "bg-gradient-to-br from-pink-400 via-purple-500 to-cyan-400 shadow-[0_0_25px_rgba(236,72,153,0.22)]"
            }
          `}
        >
          {isUser ? (
            <User
              size={18}
              className="text-white"
            />
          ) : (
            <>
              <div className="absolute inset-0 bg-white/10 animate-pulse" />

              <Bot
                size={18}
                className="text-white relative z-10"
              />

              <Sparkles
                size={10}
                className="absolute top-1 right-1 text-white/80"
              />
            </>
          )}
        </div>

        {/* CONTENT */}
        <div className="flex flex-col min-w-0">
          {/* NAME + TIME */}
          <div
            className={`
              flex items-center gap-2 mb-1 px-1
              ${
                isUser
                  ? "justify-end"
                  : "justify-start"
              }
            `}
          >
            <span
              className={`text-[11px] ${
                isUser
                  ? "text-cyan-300"
                  : "text-pink-300"
              }`}
            >
              {isUser
                ? "You"
                : "LIAO"}
            </span>

            {time && (
              <span className="text-[10px] text-slate-500">
                {time}
              </span>
            )}
          </div>

          {/* BUBBLE */}
          <div
            className={`
              group relative
              px-4 py-3
              rounded-3xl
              text-sm sm:text-[15px]
              leading-relaxed
              whitespace-pre-wrap
              break-words
              backdrop-blur-xl
              border
              ${
                isUser
                  ? `
                  text-white
                  border-cyan-300/10
                  bg-gradient-to-r from-cyan-500 to-purple-500
                  shadow-[0_0_18px_rgba(34,211,238,0.18)]
                  rounded-br-md
                `
                  : `
                  text-white
                  border-white/[0.06]
                  bg-gradient-to-br from-[#131a2c]/95 to-[#0b1120]/92
                  shadow-[0_0_18px_rgba(255,255,255,0.03)]
                  rounded-bl-md
                `
              }
            `}
          >
            {/* AI ICON */}
            {!isUser && (
              <div className="absolute top-2 right-2 opacity-40">
                <Sparkles
                  size={12}
                  className="text-pink-300"
                />
              </div>
            )}

            {/* TEXT */}
            <div className="pr-5">
              {text}
            </div>

            {/* COPY BUTTON */}
            {!isUser && text && (
              <button
                onClick={copyMessage}
                className="
                  absolute bottom-2 right-2
                  opacity-0 group-hover:opacity-100
                  transition
                  p-1 rounded-lg
                  hover:bg-white/5
                "
              >
                {copied ? (
                  <Check
                    size={14}
                    className="text-green-300"
                  />
                ) : (
                  <Copy
                    size={14}
                    className="text-slate-400"
                  />
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}