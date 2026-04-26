import { motion } from "framer-motion";
import {
  Heart,
  Sparkles,
  AudioLines,
  Stars,
} from "lucide-react";

export default function Avatar1({
  isActive = true,
}) {
  return (
    <div
      className="
        relative
        flex items-center justify-center
        w-[300px] h-[300px]
        sm:w-[380px] sm:h-[380px]
        md:w-[460px] md:h-[460px]
      "
    >
      {/* ================= BACKGROUND AMBIENT GLOW ================= */}
      <div className="absolute w-[620px] h-[620px] bg-cyan-500/10 blur-[180px] rounded-full" />
      <div className="absolute w-[520px] h-[520px] bg-purple-500/10 blur-[170px] rounded-full" />
      <div className="absolute w-[420px] h-[420px] bg-pink-500/10 blur-[150px] rounded-full" />

      {/* ================= OUTER ENERGY FIELD ================= */}
      <motion.div
        className="
          absolute
          w-[280px] h-[280px]
          sm:w-[360px] sm:h-[360px]
          md:w-[430px] md:h-[430px]
          rounded-full
          border border-cyan-300/10
        "
        animate={{ rotate: 360 }}
        transition={{
          repeat: Infinity,
          duration: 24,
          ease: "linear",
        }}
      />

      {/* SECOND RING */}
      <motion.div
        className="
          absolute
          w-[240px] h-[240px]
          sm:w-[310px] sm:h-[310px]
          md:w-[380px] md:h-[380px]
          rounded-full
          border border-purple-300/10
        "
        animate={{ rotate: -360 }}
        transition={{
          repeat: Infinity,
          duration: 18,
          ease: "linear",
        }}
      />

      {/* FLOATING PARTICLE RING */}
      <motion.div
        className="
          absolute
          w-[310px] h-[310px]
          sm:w-[400px] sm:h-[400px]
          md:w-[470px] md:h-[470px]
          rounded-full
          border border-white/5
        "
        animate={{ rotate: 360 }}
        transition={{
          repeat: Infinity,
          duration: 35,
          ease: "linear",
        }}
      >
        <span className="absolute top-2 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-cyan-300 shadow-[0_0_12px_rgba(34,211,238,.95)]" />
        <span className="absolute bottom-8 right-12 w-2 h-2 rounded-full bg-pink-300 shadow-[0_0_12px_rgba(244,114,182,.95)]" />
        <span className="absolute left-8 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-violet-300 shadow-[0_0_12px_rgba(168,85,247,.95)]" />
      </motion.div>

      {/* ================= VOICE WAVE ================= */}
      <motion.div
        className="
          absolute
          w-[150px] h-[150px]
          sm:w-[190px] sm:h-[190px]
          md:w-[230px] md:h-[230px]
          rounded-full
          border border-cyan-300/20
        "
        animate={
          isActive
            ? {
                scale: [1, 1.65, 1],
                opacity: [0.45, 0, 0.45],
              }
            : {
                scale: [1, 1.15, 1],
                opacity: [0.18, 0, 0.18],
              }
        }
        transition={{
          repeat: Infinity,
          duration: isActive ? 2 : 4,
          ease: "easeOut",
        }}
      />

      {/* ================= CORE GLOW ================= */}
      <motion.div
        className="
          absolute
          w-[140px] h-[140px]
          sm:w-[180px] sm:h-[180px]
          md:w-[220px] md:h-[220px]
          rounded-full
          bg-gradient-to-br
          from-cyan-400
          via-purple-500
          to-pink-500
          blur-2xl
          opacity-90
        "
        animate={{
          scale: [1, 1.08, 1],
          opacity: [0.72, 1, 0.72],
        }}
        transition={{
          repeat: Infinity,
          duration: 2.8,
          ease: "easeInOut",
        }}
      />

      {/* ================= GLASS CENTER ================= */}
      <div
        className="
          absolute
          w-[135px] h-[135px]
          sm:w-[170px] sm:h-[170px]
          md:w-[205px] md:h-[205px]
          rounded-full
          border border-white/10
          bg-white/[0.05]
          backdrop-blur-2xl
          shadow-[0_0_35px_rgba(0,0,0,.22)]
          flex flex-col items-center justify-center
          overflow-hidden
        "
      >
        {/* subtle light */}
        <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />

        {/* hologram icon */}
        <motion.div
          animate={{ y: [0, -5, 0] }}
          transition={{
            repeat: Infinity,
            duration: 2.6,
          }}
          className="relative z-10 flex flex-col items-center"
        >
          <div className="relative">
            <div className="w-9 h-9 sm:w-10 sm:h-10 md:w-11 md:h-11 rounded-full bg-white/90" />

            <Sparkles
              size={12}
              className="absolute -top-1 -right-4 text-cyan-300"
            />
          </div>

          <div className="w-12 h-6 sm:w-14 sm:h-7 md:w-16 md:h-8 rounded-full bg-white/75 mt-1" />
        </motion.div>

        {/* text */}
        <div className="relative z-10 text-center mt-3">
          <h2 className="text-white text-sm sm:text-base md:text-lg font-semibold tracking-[0.22em]">
            LIAO
          </h2>

          <p className="text-[10px] text-gray-300 mt-1 tracking-[0.28em] uppercase">
            AI Companion
          </p>
        </div>

        {/* mini icons */}
        <Heart
          size={12}
          className="absolute bottom-6 left-6 text-pink-300/90"
        />

        <AudioLines
          size={12}
          className="absolute top-6 left-6 text-cyan-300/90"
        />

        <Stars
          size={12}
          className="absolute top-6 right-6 text-purple-300/90"
        />
      </div>

      {/* FLOOR LIGHT */}
      <div className="absolute bottom-8 w-36 sm:w-44 md:w-56 h-7 bg-cyan-400/10 blur-2xl rounded-full" />
    </div>
  );
}