import { motion } from "framer-motion";
import {
  Heart,
  Sparkles,
} from "lucide-react";

export default function Orb({
  isActive = true,
}) {
  return (
    <div className="relative flex items-center justify-center w-[280px] h-[280px] sm:w-[340px] sm:h-[340px] md:w-[420px] md:h-[420px]">
      {/* BACKGROUND MATCHED GLOW */}
      <div className="absolute w-[520px] h-[520px] bg-cyan-500/12 blur-[170px] rounded-full" />
      <div className="absolute w-[480px] h-[480px] bg-violet-500/12 blur-[170px] rounded-full" />
      <div className="absolute w-[420px] h-[420px] bg-pink-500/10 blur-[150px] rounded-full" />

      {/* OUTER RING */}
      <motion.div
        className="absolute w-[240px] h-[240px] sm:w-[300px] sm:h-[300px] md:w-[390px] md:h-[390px] rounded-full border border-cyan-300/10"
        animate={{ rotate: 360 }}
        transition={{
          repeat: Infinity,
          duration: 26,
          ease: "linear",
        }}
      />

      {/* MID RING */}
      <motion.div
        className="absolute w-[210px] h-[210px] sm:w-[260px] sm:h-[260px] md:w-[340px] md:h-[340px] rounded-full border border-violet-300/10"
        animate={{ rotate: -360 }}
        transition={{
          repeat: Infinity,
          duration: 18,
          ease: "linear",
        }}
      />

      {/* PARTICLE RING */}
      <motion.div
        className="absolute w-[260px] h-[260px] sm:w-[330px] sm:h-[330px] md:w-[430px] md:h-[430px] rounded-full border border-white/5"
        animate={{ rotate: 360 }}
        transition={{
          repeat: Infinity,
          duration: 34,
          ease: "linear",
        }}
      >
        <span className="absolute top-2 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(34,211,238,0.9)]" />
        <span className="absolute bottom-6 right-10 w-2 h-2 rounded-full bg-pink-300 shadow-[0_0_10px_rgba(244,114,182,0.9)]" />
        <span className="absolute left-6 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-violet-300 shadow-[0_0_10px_rgba(139,92,246,0.9)]" />
      </motion.div>

      {/* SPEAKING WAVE */}
      <motion.div
        className="absolute w-[150px] h-[150px] sm:w-[190px] sm:h-[190px] md:w-[230px] md:h-[230px] rounded-full border border-cyan-400/10"
        animate={
          isActive
            ? {
                scale: [1, 1.65, 1],
                opacity: [0.4, 0, 0.4],
              }
            : {
                scale: [1, 1.15, 1],
                opacity: [0.2, 0, 0.2],
              }
        }
        transition={{
          repeat: Infinity,
          duration: isActive ? 2.1 : 4,
        }}
      />

      {/* ENERGY CORE */}
      <motion.div
        className="absolute w-[130px] h-[130px] sm:w-[155px] sm:h-[155px] md:w-[185px] md:h-[185px] rounded-full bg-gradient-to-br from-cyan-400 via-violet-500 to-pink-500 blur-xl opacity-90"
        animate={
          isActive
            ? {
                scale: [1, 1.1, 1],
                opacity: [0.72, 1, 0.72],
              }
            : {
                scale: [1, 1.03, 1],
                opacity: [0.55, 0.75, 0.55],
              }
        }
        transition={{
          repeat: Infinity,
          duration: 2.5,
          ease: "easeInOut",
        }}
      />

      {/* GLASS CENTER */}
      <div
        className="
          absolute
          w-[118px] h-[118px]
          sm:w-[140px] sm:h-[140px]
          md:w-[165px] md:h-[165px]
          rounded-full
          border border-white/10
          bg-white/[0.06]
          backdrop-blur-2xl
          flex flex-col items-center justify-center
          shadow-[0_0_35px_rgba(139,92,246,0.20)]
        "
      >
        {/* GIRL HOLOGRAM */}
        <motion.div
          animate={{ y: [0, -4, 0] }}
          transition={{
            repeat: Infinity,
            duration: 2.4,
          }}
          className="relative flex flex-col items-center"
        >
          <div className="w-8 h-8 sm:w-9 sm:h-9 md:w-10 md:h-10 rounded-full bg-white/90 mb-1" />
          <div className="w-10 h-5 sm:w-12 sm:h-6 md:w-14 md:h-7 rounded-full bg-white/75" />

          <Sparkles
            size={12}
            className="absolute -top-1 -right-4 text-cyan-300"
          />

          <Heart
            size={12}
            className="absolute bottom-0 -left-4 text-pink-300"
          />
        </motion.div>

        <p className="text-white text-xs sm:text-sm font-semibold mt-2 tracking-wide">
          Nilima
        </p>

        <p className="text-[9px] sm:text-[10px] text-pink-200/80 tracking-[0.28em] uppercase">
          Companion
        </p>
      </div>

      {/* FLOOR LIGHT */}
      <div className="absolute bottom-6 md:bottom-10 w-28 sm:w-36 md:w-44 h-6 bg-cyan-500/10 blur-2xl rounded-full" />
    </div>
  );
}