import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";
import {
  X,
  Volume2,
  Moon,
  Mic,
  Cpu,
  Trash2,
  Shield,
  Sparkles,
} from "lucide-react";

/* ==================================================
   ⚙️ SETTINGS PANEL
================================================== */
export default function SettingsPanel({
  isOpen,
  onClose,
  onClearChat,
}) {
  const [voice, setVoice] = useState(true);
  const [darkMode, setDarkMode] = useState(true);
  const [autoListen, setAutoListen] = useState(false);
  const [provider, setProvider] = useState("auto");
  const [animations, setAnimations] = useState(true);
  const [secureMode, setSecureMode] = useState(true);

  /* ==================================================
     💾 LOAD SAVED SETTINGS
  ================================================== */
  useEffect(() => {
    const saved = localStorage.getItem("liao_settings");

    if (saved) {
      try {
        const data = JSON.parse(saved);

        setVoice(data.voice ?? true);
        setDarkMode(data.darkMode ?? true);
        setAutoListen(data.autoListen ?? false);
        setProvider(data.provider ?? "auto");
        setAnimations(data.animations ?? true);
        setSecureMode(data.secureMode ?? true);
      } catch {}
    }
  }, []);

  /* ==================================================
     💾 SAVE SETTINGS
  ================================================== */
  useEffect(() => {
    localStorage.setItem(
      "liao_settings",
      JSON.stringify({
        voice,
        darkMode,
        autoListen,
        provider,
        animations,
        secureMode,
      })
    );

    document.documentElement.classList.toggle(
      "dark",
      darkMode
    );
  }, [
    voice,
    darkMode,
    autoListen,
    provider,
    animations,
    secureMode,
  ]);

  /* ==================================================
     🚫 CLOSE ON ESC
  ================================================== */
  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handleKey);

    return () =>
      window.removeEventListener(
        "keydown",
        handleKey
      );
  }, [onClose]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="absolute inset-0 z-50 flex justify-end">

          {/* ==========================================
             🔲 BACKDROP
          ========================================== */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
          />

          {/* ==========================================
             ⚙️ PANEL
          ========================================== */}
          <motion.div
            initial={{ x: 450 }}
            animate={{ x: 0 }}
            exit={{ x: 450 }}
            transition={{
              type: "spring",
              damping: 22,
              stiffness: 180,
            }}
            className="relative w-[420px] h-full bg-[#0B1120]/95 backdrop-blur-2xl border-l border-white/10 p-6 overflow-y-auto shadow-[0_0_60px_rgba(0,255,255,0.08)]"
          >
            {/* ======================================
               🔝 HEADER
            ====================================== */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-xl font-semibold tracking-wide">
                  Settings
                </h2>

                <p className="text-sm text-gray-400 mt-1">
                  Customize your AI assistant
                </p>
              </div>

              <button
                onClick={onClose}
                className="p-2 rounded-full hover:bg-white/10 transition"
              >
                <X size={18} />
              </button>
            </div>

            {/* ======================================
               ⚙️ OPTIONS
            ====================================== */}
            <div className="space-y-6">

              <Section title="Assistant">

                <Toggle
                  icon={Volume2}
                  label="Voice Response"
                  desc="AI speaks replies aloud"
                  value={voice}
                  onChange={setVoice}
                />

                <Toggle
                  icon={Mic}
                  label="Auto Listening"
                  desc="Enable microphone mode"
                  value={autoListen}
                  onChange={setAutoListen}
                />

                <Toggle
                  icon={Sparkles}
                  label="Animations"
                  desc="Enable UI effects"
                  value={animations}
                  onChange={setAnimations}
                />

              </Section>

              <Section title="Appearance">

                <Toggle
                  icon={Moon}
                  label="Dark Mode"
                  desc="Premium dark interface"
                  value={darkMode}
                  onChange={setDarkMode}
                />

              </Section>

              <Section title="AI Provider">

                <ProviderButton
                  label="Auto"
                  active={provider === "auto"}
                  onClick={() =>
                    setProvider("auto")
                  }
                />

                <ProviderButton
                  label="Groq"
                  active={provider === "groq"}
                  onClick={() =>
                    setProvider("groq")
                  }
                />

                <ProviderButton
                  label="Gemini"
                  active={provider === "gemini"}
                  onClick={() =>
                    setProvider("gemini")
                  }
                />

                <ProviderButton
                  label="Mistral"
                  active={provider === "mistral"}
                  onClick={() =>
                    setProvider("mistral")
                  }
                />

              </Section>

              <Section title="Security">

                <Toggle
                  icon={Shield}
                  label="Secure Mode"
                  desc="Safer system actions"
                  value={secureMode}
                  onChange={setSecureMode}
                />

              </Section>

              <Section title="System">

                <button
                  onClick={onClearChat}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 transition"
                >
                  <Trash2 size={18} />
                  <span className="text-sm">
                    Clear Chat History
                  </span>
                </button>

              </Section>

            </div>

            {/* ======================================
               FOOTER
            ====================================== */}
            <div className="mt-10 pt-6 border-t border-white/10 text-xs text-gray-500 flex items-center gap-2">
              <Cpu size={14} />
              LIAO AI Control Center
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

/* ==================================================
   🧩 SECTION
================================================== */
function Section({ title, children }) {
  return (
    <div className="space-y-3">
      <h3 className="text-xs uppercase tracking-[0.25em] text-gray-500">
        {title}
      </h3>

      <div className="space-y-3">
        {children}
      </div>
    </div>
  );
}

/* ==================================================
   🔁 TOGGLE
================================================== */
function Toggle({
  icon: Icon,
  label,
  desc,
  value,
  onChange,
}) {
  return (
    <div className="flex items-center justify-between rounded-2xl bg-white/5 border border-white/5 px-4 py-3">

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center">
          <Icon size={18} />
        </div>

        <div>
          <p className="text-sm font-medium">
            {label}
          </p>

          <p className="text-xs text-gray-400">
            {desc}
          </p>
        </div>
      </div>

      <motion.div
        onClick={() => onChange(!value)}
        className={`w-12 h-6 rounded-full px-1 flex items-center cursor-pointer transition ${
          value
            ? "bg-cyan-500 justify-end"
            : "bg-gray-600 justify-start"
        }`}
      >
        <motion.div
          layout
          className="w-4 h-4 bg-white rounded-full"
        />
      </motion.div>

    </div>
  );
}

/* ==================================================
   🤖 PROVIDER BUTTON
================================================== */
function ProviderButton({
  label,
  active,
  onClick,
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full px-4 py-3 rounded-xl text-sm transition border ${
        active
          ? "bg-cyan-500/15 border-cyan-400/30 text-white"
          : "bg-white/5 border-white/5 text-gray-400 hover:bg-white/10"
      }`}
    >
      {label}
    </button>
  );
}