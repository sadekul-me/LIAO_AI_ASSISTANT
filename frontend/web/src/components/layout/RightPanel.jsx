import { motion } from "framer-motion";
import SystemBar from "../dashboard/SystemBar";
import SystemOverview from "../dashboard/SystemOverview";
import QuickActions from "../dashboard/QuickActions";
import RecentActivities from "../dashboard/RecentActivities";
import VoiceAssistant from "../voice/VoiceAssistant";

const RightPanel = () => {

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.12,
        delayChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 30, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 110,
        damping: 18,
      },
    },
  };

  return (
    <motion.aside
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="
        relative h-full w-full
        flex flex-col
        gap-3
        overflow-hidden
        bg-gradient-to-b from-[#080E1C] via-[#050914] to-[#03060E]
        p-2
        z-10
        border-l border-white/5
      "
    >

      {/* 🔮 ULTRA GLOW: সাইডবারের সায়ান থিমের সাথে সিঙ্ক করা */}
      <motion.div
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.2, 0.35, 0.2],
        }}
        transition={{ duration: 6, repeat: Infinity }}
        className="absolute bottom-[-10%] right-[-10%] w-[70%] h-[50%] bg-cyan-600/10 blur-[120px] rounded-full pointer-events-none z-0"
      />

      {/* 🔹 SYSTEM BAR */}
      <motion.div variants={itemVariants} className="relative z-10">
        <SystemBar />
      </motion.div>

      {/* 🔹 MAIN STACK */}
      <div className="relative z-10 flex flex-col gap-3">

        {/* System Overview */}
        <motion.div
          variants={itemVariants}
          className="rounded-[28px] overflow-hidden border border-white/[0.06] bg-[#1E293B]/10 backdrop-blur-sm shadow-lg"
        >
          <SystemOverview />
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          variants={itemVariants}
          className="rounded-[28px] overflow-hidden border border-white/[0.06] bg-[#1E293B]/10 backdrop-blur-sm shadow-lg"
        >
          <QuickActions />
        </motion.div>

        {/* Recent Activities */}
        <motion.div
          variants={itemVariants}
          className="rounded-[28px] overflow-hidden border border-white/[0.06] bg-[#1E293B]/10 backdrop-blur-sm shadow-lg"
        >
          <RecentActivities />
        </motion.div>

      </div>

      {/* 🎙️ VOICE ASSISTANT (Fixed flex area) */}
      <motion.div
        variants={itemVariants}
        className="flex-1 min-h-0 flex relative z-10"
      >
        <div className="w-full h-full rounded-[32px] overflow-hidden border border-white/[0.08] bg-[#1E293B]/15 shadow-2xl backdrop-blur-md">
          <VoiceAssistant />
        </div>
      </motion.div>

    </motion.aside>
  );
};

export default RightPanel;