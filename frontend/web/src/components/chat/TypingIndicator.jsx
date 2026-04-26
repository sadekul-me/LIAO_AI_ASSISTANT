import { motion } from "framer-motion";
import {
  BrainCircuit,
  Sparkles,
  Bot,
} from "lucide-react";

const dots = [0, 1, 2];

export default function TypingIndicator() {
  return (
    <div className="flex items-end gap-3 w-full">
      {/* AVATAR */}
      <div className="relative shrink-0">
        <div
          className="
            relative
            w-10 h-10 sm:w-11 sm:h-11
            rounded-2xl
            flex items-center justify-center
            bg-gradient-to-br
            from-pink-400
            via-purple-500
            to-cyan-400
            shadow-[0_0_22px_rgba(236,72,153,0.22)]
            overflow-hidden
          "
        >
          <div className="absolute inset-0 bg-white/10 animate-pulse" />

          <Bot
            size={18}
            className="text-white relative z-10"
          />

          <Sparkles
            size={10}
            className="absolute top-1 right-1 text-white/80"
          />
        </div>

        {/* PULSE RING */}
        <motion.div
          animate={{
            scale: [1, 1.35, 1],
            opacity: [0.35, 0, 0.35],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
          }}
          className="absolute inset-0 rounded-2xl bg-cyan-400/20"
        />
      </div>

      {/* BUBBLE */}
      <motion.div
        initial={{
          opacity: 0,
          x: -10,
          scale: 0.96,
        }}
        animate={{
          opacity: 1,
          x: 0,
          scale: 1,
        }}
        className="
          relative
          max-w-[280px] sm:max-w-[320px]
          rounded-3xl rounded-bl-md
          border border-white/[0.06]
          bg-gradient-to-br from-[#131a2c]/95 to-[#0b1120]/92
          backdrop-blur-2xl
          px-4 sm:px-5 py-3
          shadow-[0_10px_35px_rgba(0,0,0,0.25)]
          overflow-hidden
        "
      >
        {/* TOP GLOW */}
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent" />

        {/* HEADER */}
        <div className="flex items-center gap-2 mb-2">
          <motion.div
            animate={{
              rotate: 360,
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "linear",
            }}
          >
            <BrainCircuit
              size={13}
              className="text-cyan-400"
            />
          </motion.div>

          <span className="text-[10px] uppercase tracking-[0.25em] text-slate-400 font-semibold">
            Thinking
          </span>
        </div>

        {/* DOTS */}
        <div className="flex items-center gap-2">
          {dots.map((dot) => (
            <motion.span
              key={dot}
              animate={{
                y: [0, -5, 0],
                opacity: [0.4, 1, 0.4],
                scale: [1, 1.15, 1],
              }}
              transition={{
                duration: 1.1,
                repeat: Infinity,
                delay: dot * 0.18,
              }}
              className={`
                w-1.5 h-1.5 rounded-full
                ${
                  dot === 0
                    ? "bg-cyan-400"
                    : dot === 1
                    ? "bg-blue-400"
                    : "bg-purple-400"
                }
              `}
            />
          ))}

          <motion.span
            animate={{
              opacity: [0.45, 1, 0.45],
            }}
            transition={{
              duration: 1.6,
              repeat: Infinity,
            }}
            className="ml-2 text-[11px] text-cyan-300/80 italic"
          >
            Processing...
          </motion.span>
        </div>

        {/* BOTTOM BEAM */}
        <motion.div
          animate={{
            x: [
              "-100%",
              "220%",
            ],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "linear",
          }}
          className="
            absolute bottom-0 left-0
            h-px w-full
            bg-gradient-to-r
            from-transparent
            via-cyan-400/40
            to-transparent
          "
        />
      </motion.div>
    </div>
  );
}