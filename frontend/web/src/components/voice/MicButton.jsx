import { motion, AnimatePresence } from "framer-motion";
import { Mic, MicOff, Loader2, Volume2 } from "lucide-react";

const MicButton = ({
  active = false,
  thinking = false,
  speaking = false,
  disabled = false,
  onClick = () => {},
}) => {
  const getGlowClass = () => {
    if (disabled) return "bg-slate-500/20";
    if (active) return "bg-cyan-500/40";
    if (thinking) return "bg-yellow-500/40";
    if (speaking) return "bg-emerald-500/40";
    return "bg-cyan-500/20";
  };

  const getGradient = () => {
    if (disabled) {
      return "linear-gradient(135deg,#334155 0%,#1e293b 100%)";
    }

    if (active) {
      return "linear-gradient(135deg,#06b6d4 0%,#2563eb 100%)";
    }

    if (thinking) {
      return "linear-gradient(135deg,#f59e0b 0%,#f97316 100%)";
    }

    if (speaking) {
      return "linear-gradient(135deg,#10b981 0%,#059669 100%)";
    }

    return "linear-gradient(135deg,#22d3ee 0%,#3b82f6 50%,#9333ea 100%)";
  };

  const renderIcon = () => {
    if (disabled) return <MicOff size={20} />;
    if (thinking) return <Loader2 size={20} className="animate-spin" />;
    if (speaking) return <Volume2 size={20} />;
    if (active) return <MicOff size={20} />;
    return <Mic size={20} />;
  };

  const title = disabled
    ? "Voice not supported"
    : active
    ? "Stop listening"
    : "Start voice";

  return (
    <motion.button
      type="button"
      title={title}
      disabled={disabled}
      onClick={onClick}
      whileHover={!disabled ? { scale: 1.05 } : {}}
      whileTap={!disabled ? { scale: 0.92 } : {}}
      className="
        relative
        flex items-center justify-center
        w-12 h-12
        rounded-full
        z-20
        outline-none
        disabled:cursor-not-allowed
      "
    >
      {/* Glow */}
      <motion.div
        animate={{
          opacity: 1,
          scale: active || thinking || speaking ? [1, 1.15, 1] : 1,
        }}
        transition={{
          duration: 1.8,
          repeat: Infinity,
        }}
        className={`
          absolute inset-0 rounded-full blur-xl
          ${getGlowClass()}
        `}
      />

      {/* Main Gradient */}
      <motion.div
        animate={{
          rotate: active || thinking || speaking ? 180 : 0,
          background: getGradient(),
        }}
        transition={{
          duration: 0.5,
        }}
        className="
          absolute inset-0 rounded-full
          border border-white/20
          shadow-[0_0_30px_rgba(0,0,0,0.45)]
        "
      />

      {/* Glass Ring */}
      <div
        className="
          absolute inset-1 rounded-full
          border border-white/10
          bg-white/5
          backdrop-blur-sm
          z-10
        "
      />

      {/* Icon */}
      <AnimatePresence mode="wait">
        <motion.div
          key={`${active}-${thinking}-${speaking}-${disabled}`}
          initial={{ scale: 0, rotate: -90 }}
          animate={{ scale: 1, rotate: 0 }}
          exit={{ scale: 0, rotate: 90 }}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 20,
          }}
          className="
            relative z-20 text-white
            drop-shadow-[0_2px_4px_rgba(0,0,0,0.3)]
          "
        >
          {renderIcon()}
        </motion.div>
      </AnimatePresence>

      {/* Ripple */}
      {(active || speaking) && (
        <div className="absolute inset-0 z-0">
          {[1, 2].map((item) => (
            <motion.div
              key={item}
              initial={{ scale: 1, opacity: 0.5 }}
              animate={{ scale: 2.1, opacity: 0 }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: item * 0.35,
                ease: "easeOut",
              }}
              className="
                absolute inset-0 rounded-full
                border border-cyan-400/40
              "
            />
          ))}
        </div>
      )}

      {/* Orbit Dot */}
      {!active && !thinking && !speaking && !disabled && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute inset-[-4px] rounded-full"
        >
          <div
            className="
              w-1.5 h-1.5 rounded-full
              bg-cyan-400
              shadow-[0_0_8px_#22d3ee]
              absolute top-0 left-1/2 -translate-x-1/2
            "
          />
        </motion.div>
      )}
    </motion.button>
  );
};

export default MicButton;