import MicButton from "./MicButton";
import VoiceVisualizer from "./VoiceVisualizer";
import GlassCard from "../ui/GlassCard";

const VoiceAssistant = () => {
  return (
    <GlassCard
      className="
        flex-1 min-h-0
        h-[190px]   /* 🔥 আরও height কমানো */
        p-3
        rounded-3xl
        bg-gradient-to-br from-[#0b1220] to-[#020617]
        flex flex-col
      "
    >
      {/* 🔹 Header */}
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-semibold text-slate-300">
          Voice Assistant
        </h2>

        <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-400/20">
          Ready
        </span>
      </div>

      {/* 🔹 Body */}
      <div className="flex-1 flex flex-col items-center justify-center gap-2">
        
        {/* 🎤 Mic */}
        <div className="relative flex items-center justify-center">
          
          {/* Glow */}
          <div className="absolute w-14 h-14 rounded-full bg-cyan-500/20 blur-2xl animate-pulse" />

          {/* Ring */}
          <div className="absolute w-12 h-12 rounded-full border border-cyan-400/20" />

          <MicButton />
        </div>

        {/* 🎧 Waveform */}
        <div className="w-full flex justify-center">
          <VoiceVisualizer />
        </div>

        {/* 🔸 Status */}
        <span className="text-[10px] text-slate-400 text-center">
          Tap the mic to start speaking
        </span>
      </div>
    </GlassCard>
  );
};

export default VoiceAssistant;