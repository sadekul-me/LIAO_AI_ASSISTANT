import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import {
  Mic,
  MessageCircle,
  Zap,
  Settings,
  Wifi,
  WifiOff,
  Loader2,
  ChevronDown,
} from "lucide-react";

export default function Topbar({
  onOpenSettings,
  backendOnline = true,
  provider = "offline",
  currentMode = "chat",
  onModeChange,
}) {
  const [activeMode, setActiveMode] = useState(currentMode);
  const [time, setTime] = useState("");

  const modes = [
    {
      id: "chat",
      label: "Chat",
      icon: MessageCircle,
    },
    {
      id: "voice",
      label: "Voice",
      icon: Mic,
    },
    {
      id: "command",
      label: "Command",
      icon: Zap,
    },
  ];

  useEffect(() => {
    setActiveMode(currentMode);
  }, [currentMode]);

  useEffect(() => {
    updateClock();

    const timer = setInterval(() => {
      updateClock();
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const updateClock = () => {
    const now = new Date();

    setTime(
      now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    );
  };

  const handleModeChange = (modeId) => {
    setActiveMode(modeId);
    onModeChange?.(modeId);
  };

  const getProviderColor = () => {
    if (provider === "groq") return "text-cyan-300";
    if (provider === "gemini") return "text-purple-300";
    if (provider === "offline") return "text-yellow-300";
    if (provider === "loading") return "text-white";
    return "text-gray-300";
  };

  const getProviderText = () => {
    if (provider === "groq") return "Groq";
    if (provider === "gemini") return "Gemini";
    if (provider === "offline") return "Offline";
    if (provider === "loading") return "Loading";
    return "Unknown";
  };

  return (
    <header
      className="
        absolute top-0 left-0 w-full h-[72px]
        px-5 md:px-7
        flex items-center justify-between
        z-50
        border-b border-white/10
        bg-[#08111f]/72
        backdrop-blur-3xl
      "
    >
      {/* PREMIUM TOP GLOW */}
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent" />

      {/* LEFT */}
      <div className="flex items-center gap-3 min-w-[180px]">
        {/* LOGO */}
        <motion.div
          animate={{
            rotate: backendOnline ? 360 : 0,
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "linear",
          }}
          className="
            relative
            w-11 h-11 rounded-2xl
            bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-500
            shadow-[0_0_24px_rgba(34,211,238,0.22)]
            flex items-center justify-center
          "
        >
          <div className="w-5 h-5 rounded-full bg-white/90" />

          <div className="absolute inset-0 rounded-2xl border border-white/10" />
        </motion.div>

        {/* TITLE */}
        <div className="leading-tight">
          <h1 className="text-white text-sm font-semibold tracking-[0.32em]">
            LIAO
          </h1>

          <p className="text-[10px] text-gray-400 tracking-[0.22em] uppercase">
            Premium AI Core
          </p>
        </div>
      </div>

      {/* CENTER MODE SWITCHER */}
      <div
        className="
          hidden md:flex
          items-center gap-2
          p-1.5 rounded-full
          border border-white/10
          bg-white/[0.04]
          backdrop-blur-xl
        "
      >
        {modes.map((mode) => {
          const Icon = mode.icon;
          const isActive = activeMode === mode.id;

          return (
            <motion.button
              key={mode.id}
              whileTap={{ scale: 0.94 }}
              whileHover={{ y: -1 }}
              onClick={() => handleModeChange(mode.id)}
              className={`
                relative
                px-4 py-2 rounded-full
                text-sm flex items-center gap-2
                transition-all duration-300
                ${
                  isActive
                    ? "text-white"
                    : "text-gray-300 hover:text-white"
                }
              `}
            >
              {isActive && (
                <motion.div
                  layoutId="mode-pill"
                  className="
                    absolute inset-0 rounded-full
                    bg-gradient-to-r from-cyan-500 to-purple-500
                    shadow-[0_0_18px_rgba(34,211,238,0.25)]
                  "
                  transition={{
                    type: "spring",
                    stiffness: 280,
                    damping: 24,
                  }}
                />
              )}

              <span className="relative z-10 flex items-center gap-2">
                <Icon size={15} />
                {mode.label}
              </span>
            </motion.button>
          );
        })}
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-3 md:gap-4 min-w-[220px] justify-end">
        {/* TIME */}
        <div className="hidden lg:block text-sm text-gray-400 font-medium">
          {time}
        </div>

        {/* PROVIDER */}
        <div
          className={`
            hidden md:flex items-center gap-2
            px-3 py-2 rounded-full
            border border-white/10
            bg-white/[0.04]
            text-sm ${getProviderColor()}
          `}
        >
          {provider === "loading" ? (
            <Loader2
              size={14}
              className="animate-spin"
            />
          ) : backendOnline ? (
            <Wifi size={14} />
          ) : (
            <WifiOff size={14} />
          )}

          <span>{getProviderText()}</span>
        </div>

        {/* STATUS */}
        <div
          className="
            hidden sm:flex items-center gap-2
            px-3 py-2 rounded-full
            border border-white/10
            bg-white/[0.04]
          "
        >
          <span
            className={`
              w-2 h-2 rounded-full animate-pulse
              ${
                backendOnline
                  ? "bg-green-400"
                  : "bg-red-400"
              }
            `}
          />

          <span
            className={`text-sm ${
              backendOnline
                ? "text-green-300"
                : "text-red-300"
            }`}
          >
            {backendOnline
              ? "Online"
              : "Offline"}
          </span>
        </div>

        {/* SETTINGS */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          whileHover={{ rotate: 90 }}
          transition={{ duration: 0.22 }}
          onClick={onOpenSettings}
          className="
            w-11 h-11 rounded-2xl
            flex items-center justify-center
            border border-white/10
            bg-white/[0.05]
            hover:bg-white/[0.09]
            text-white
            transition-all
          "
        >
          <Settings size={18} />
        </motion.button>

        {/* MOBILE MODE */}
        <div className="md:hidden">
          <button
            className="
              w-10 h-10 rounded-2xl
              flex items-center justify-center
              border border-white/10
              bg-white/[0.05]
              text-white
            "
          >
            <ChevronDown size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}