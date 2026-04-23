import { motion } from "framer-motion";

/**
 * props:
 * isListening = true হলে active animation
 */
export default function VoiceWave({ isListening = false }) {
  const bars = [1, 2, 3, 4, 5, 6];

  return (
    <div className="flex items-center justify-center gap-1 mt-4">

      {bars.map((bar) => (
        <motion.div
          key={bar}
          className="w-[4px] rounded-full bg-gradient-to-t from-cyan-400 to-purple-500"
          animate={
            isListening
              ? {
                  height: [10, 30, 15, 40, 12],
                  opacity: [0.6, 1, 0.8, 1, 0.6],
                }
              : {
                  height: [8, 12, 8],
                  opacity: [0.5, 0.8, 0.5],
                }
          }
          transition={{
            duration: isListening ? 1.2 : 2,
            repeat: Infinity,
            delay: bar * 0.1,
          }}
        />
      ))}

    </div>
  );
}