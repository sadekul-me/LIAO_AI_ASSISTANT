import { motion, AnimatePresence } from "framer-motion";
import { Mic, MicOff } from "lucide-react";

const MicButton = ({ active = false, onToggle }) => {
  return (
    <motion.button
      onClick={onToggle}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.92 }}
      className="relative flex items-center justify-center w-12 h-12 rounded-full z-20 group"
    >
      {/* 🔮 Ultra Glow Layer: অ্যাক্টিভ মোডে লাল এবং অফ মোডে সায়ান গ্লো */}
      <AnimatePresence>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ 
            opacity: 1,
            scale: active ? [1, 1.2, 1] : 1 
          }}
          transition={{ duration: 2, repeat: Infinity }}
          className={`absolute inset-0 rounded-full blur-xl ${
            active ? "bg-red-500/40" : "bg-cyan-500/20"
          }`}
        />
      </AnimatePresence>

      {/* 🌀 Dynamic Background Gradient */}
      <motion.div
        animate={{
          rotate: active ? 180 : 0,
          background: active 
            ? "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)" 
            : "linear-gradient(135deg, #22d3ee 0%, #3b82f6 50%, #9333ea 100%)",
        }}
        className="absolute inset-0 rounded-full shadow-[0_0_30px_rgba(0,0,0,0.5)] border border-white/20"
      />

      {/* ⚡ Glassmorphic Inner Ring */}
      <div className="absolute inset-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-[2px] z-10" />

      {/* 🎙️ Icon with Morphing Effect */}
      <motion.div
        key={active ? "active" : "inactive"}
        initial={{ scale: 0, rotate: -90 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
        className="relative z-20 text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]"
      >
        {active ? <MicOff size={20} /> : <Mic size={20} />}
      </motion.div>

      {/* 🌊 Active Ripple Effect: শুধুমাত্র যখন কথা বলবে */}
      {active && (
        <div className="absolute inset-0 z-0">
          {[1, 2].map((i) => (
            <motion.div
              key={i}
              initial={{ scale: 1, opacity: 0.5 }}
              animate={{ scale: 2.2, opacity: 0 }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.4,
                ease: "easeOut",
              }}
              className="absolute inset-0 rounded-full border border-red-500/50"
            />
          ))}
        </div>
      )}

      {/* ✨ Orbiting Particle (Pro Detail) */}
      {!active && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
          className="absolute inset-[-4px] rounded-full"
        >
          <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full shadow-[0_0_8px_#22d3ee] absolute top-0 left-1/2 -translate-x-1/2" />
        </motion.div>
      )}
    </motion.button>
  );
};

export default MicButton;