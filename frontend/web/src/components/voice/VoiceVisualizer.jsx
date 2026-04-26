import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";

const VoiceVisualizer = ({ active = false, stream = null, bars = 24 }) => {
  const rafRef = useRef(null);
  const analyserRef = useRef(null);
  const dataRef = useRef(null);

  // ডিফল্ট ছোট হাইট যাতে 'Ready' মোডে হালকা ভাইব থাকে
  const [heights, setHeights] = useState(
    Array.from({ length: bars }, () => 0.1)
  );

  useEffect(() => {
    if (!stream) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioContext();
    const analyser = ctx.createAnalyser();
    analyser.fftSize = 256; // High precision
    analyser.smoothingTimeConstant = 0.8; // Smooth transition

    const source = ctx.createMediaStreamSource(stream);
    source.connect(analyser);
    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    analyserRef.current = analyser;
    dataRef.current = dataArray;

    return () => ctx.close();
  }, [stream]);

  useEffect(() => {
    const animate = () => {
      setHeights((prev) => {
        let next = [];
        if (active && analyserRef.current && dataRef.current) {
          analyserRef.current.getByteFrequencyData(dataRef.current);
          const chunk = Math.floor(dataRef.current.length / bars);
          
          next = Array.from({ length: bars }, (_, i) => {
            let sum = 0;
            for (let j = 0; j < chunk; j++) {
              sum += dataRef.current[i * chunk + j];
            }
            const avg = sum / chunk;
            // ম্যাপ করা হচ্ছে যাতে মাঝখানের বারগুলো বেশি লাফায় (Mirror Effect)
            const multiplier = i < bars / 2 ? (i + 1) / (bars / 2) : (bars - i) / (bars / 2);
            return Math.max(0.1, (avg / 255) * multiplier * 1.2);
          });
        } else {
          // আইডল মোডে ওয়েভ অ্যানিমেশন
          next = prev.map((h, i) => {
            const time = Date.now() / 1000;
            const wave = Math.sin(time * 2 + i * 0.5) * 0.05 + 0.1;
            return active ? wave * 2 : wave;
          });
        }
        return next;
      });
      rafRef.current = requestAnimationFrame(animate);
    };

    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
  }, [active, bars]);

  return (
    <div className="w-full h-10 flex items-center justify-center gap-[4px] relative px-4">
      {/* 🔮 Central Glow Background */}
      <AnimatePresence>
        {active && (
          <motion.div
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-cyan-500/10 blur-[30px] rounded-full"
          />
        )}
      </AnimatePresence>

      {heights.map((h, i) => (
        <motion.span
          key={i}
          animate={{ height: `${h * 100}%` }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
          className={`
            w-[3.5px] rounded-full transition-colors duration-500
            ${
              active
                ? "bg-gradient-to-t from-cyan-500 via-blue-500 to-purple-600 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                : "bg-white/10"
            }
          `}
          style={{
            // Symmetric scaling: মাঝখানে লম্বা, দুই পাশে ছোট
            opacity: 0.3 + h * 0.7,
          }}
        />
      ))}
    </div>
  );
};

import { AnimatePresence } from "framer-motion";
export default VoiceVisualizer;