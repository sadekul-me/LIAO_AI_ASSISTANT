import { motion, AnimatePresence } from "framer-motion";
import Sidebar from "./Sidebar";
import Home from "../../pages/Home";

const MainLayout = () => {
  return (
    <div className="relative flex h-screen w-full bg-[#02040A] text-white overflow-hidden font-sans">
      
      {/* 🌌 Ultra-Pro Ambient Background Engine */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {/* Top Right Glow */}
        <div className="absolute -top-[10%] -right-[5%] w-[40%] h-[40%] bg-cyan-500/5 blur-[120px] rounded-full" />
        {/* Bottom Left Glow */}
        <div className="absolute -bottom-[10%] -left-[5%] w-[30%] h-[40%] bg-purple-600/5 blur-[100px] rounded-full" />
        {/* Noise Texture Layer (Optional: Overlay for high-end feel) */}
        <div className="absolute inset-0 opacity-[0.02] bg-[url('https://grainy-gradients.vercel.app/noise.svg')] pointer-events-none" />
      </div>

      {/* 🔹 Sidebar Section: Fixed width with subtle border */}
      <motion.aside 
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative z-20"
      >
        <Sidebar />
      </motion.aside>

      {/* 🔹 Main Area: Content with smooth layout transitions */}
      <main className="relative flex-1 flex flex-col min-w-0 z-10">
        
        {/* 🔸 Page Content Wrapper */}
        <div className="flex-1 overflow-hidden relative">
          <AnimatePresence mode="wait">
            <motion.div
              key="page-content" // ভবিষ্যতে রাউটিং থাকলে এখানে location.pathname দিবে
              initial={{ opacity: 0, y: 10, scale: 0.99 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 1.01 }}
              transition={{ 
                type: "spring", 
                stiffness: 100, 
                damping: 20,
                duration: 0.5 
              }}
              className="h-full w-full"
            >
              <Home />
            </motion.div>
          </AnimatePresence>
        </div>

      </main>

      {/* 🛠 Interactive Overlay (Pro Detail) */}
      <div className="fixed inset-0 border-[8px] border-white/[0.01] pointer-events-none z-50 rounded-none" />
    </div>
  );
};

export default MainLayout;