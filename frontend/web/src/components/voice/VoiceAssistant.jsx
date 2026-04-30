import useVoice from "../../hooks/useVoice";
import MicButton from "./MicButton";
import VoiceVisualizer from "./VoiceVisualizer";
import GlassCard from "../ui/GlassCard";

const VoiceAssistant = () => {
  const {
    isSupported,
    isListening,
    isSpeaking,
    isThinking,
    transcript,
    interimTranscript,
    reply,
    error,
    toggleListening,
  } = useVoice();

  /* =========================
     STATUS TEXT
  ========================= */
  const getStatusText = () => {
    if (!isSupported) return "Not Supported";
    if (error) return "Error";
    if (isListening) return "Listening";
    if (isThinking) return "Thinking";
    if (isSpeaking) return "Speaking";
    return "Ready";
  };

  /* =========================
     STATUS COLOR (FIXED SYSTEM)
  ========================= */
  const getStatusColor = () => {
    if (!isSupported)
      return "text-red-400 bg-red-500/10 border-red-400/30";

    if (error)
      return "text-red-400 bg-red-500/10 border-red-400/30";

    if (isListening)
      return "text-cyan-300 bg-cyan-500/10 border-cyan-400/30";

    if (isThinking)
      return "text-yellow-300 bg-yellow-500/10 border-yellow-400/30";

    if (isSpeaking)
      return "text-emerald-300 bg-emerald-500/10 border-emerald-400/30";

    return "text-emerald-300 bg-emerald-500/10 border-emerald-400/20";
  };

  /* =========================
     DISPLAY TEXT
  ========================= */
  const getDisplayText = () => {
    if (error) return error;

    if (interimTranscript) return interimTranscript;

    if (transcript) return transcript;

    if (reply) return reply;

    if (isListening) return "I'm listening...";

    if (isThinking) return "Thinking...";

    if (isSpeaking) return "Speaking...";

    return "Tap the mic to start speaking";
  };

  return (
    <GlassCard
      className="
        flex-1 min-h-0
        h-[190px]
        p-3
        rounded-3xl
        flex flex-col
        overflow-hidden
        bg-gradient-to-br from-[#0b1220] to-[#020617]
      "
    >
      {/* HEADER */}
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-semibold text-slate-300">
          Voice Assistant
        </h2>

        <span
          className={`
            text-[10px]
            px-2 py-0.5
            rounded-md
            border
            transition-all duration-300
            ${getStatusColor()}
          `}
        >
          {getStatusText()}
        </span>
      </div>

      {/* BODY */}
      <div className="flex-1 flex flex-col items-center justify-center gap-2">

        {/* MIC */}
        <div className="relative flex items-center justify-center">

          {/* Glow */}
          <div
            className={`
              absolute w-16 h-16 rounded-full blur-2xl transition-all duration-300
              ${
                isListening
                  ? "bg-cyan-500/25 animate-pulse scale-110"
                  : isThinking
                  ? "bg-yellow-500/20 animate-pulse"
                  : isSpeaking
                  ? "bg-emerald-500/20 animate-pulse"
                  : "bg-cyan-500/10"
              }
            `}
          />

          {/* Ring */}
          <div
            className={`
              absolute w-14 h-14 rounded-full border transition-all duration-300
              ${
                isListening
                  ? "border-cyan-400/60 scale-110"
                  : isThinking
                  ? "border-yellow-400/60"
                  : isSpeaking
                  ? "border-emerald-400/60"
                  : "border-cyan-400/20"
              }
            `}
          />

          <MicButton
            active={isListening}
            thinking={isThinking}
            speaking={isSpeaking}
            disabled={!isSupported}
            onClick={toggleListening}
          />
        </div>

        {/* WAVE */}
        <div className="w-full flex justify-center">
          <VoiceVisualizer
            active={isListening || isSpeaking}
            thinking={isThinking}
          />
        </div>

        {/* TEXT */}
        <div className="h-[32px] flex items-center justify-center px-2">
          <span className="text-[10px] text-slate-400 text-center leading-relaxed">
            {getDisplayText()}
          </span>
        </div>

      </div>
    </GlassCard>
  );
};

export default VoiceAssistant;