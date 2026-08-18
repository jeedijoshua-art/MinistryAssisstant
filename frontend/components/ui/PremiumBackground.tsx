"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

export function PremiumBackground() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="fixed inset-0 z-[-1] overflow-hidden bg-[#0a0f18]">
      {/* Base soft dark blue gradient */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-950/40 via-[#0a0f18] to-[#05080c]" />

      {/* Very soft golden glow from top */}
      <motion.div
        animate={{ opacity: [0.15, 0.25, 0.15], scale: [1, 1.05, 1] }}
        transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
        className="absolute -top-[20%] left-1/2 h-[60vh] w-[80vw] -translate-x-1/2 rounded-[100%] bg-amber-500/10 blur-[120px]"
      />

      {/* Subtle blue depth from sides */}
      <motion.div
        animate={{ opacity: [0.2, 0.3, 0.2], x: [0, 20, 0] }}
        transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
        className="absolute -left-[10%] top-[30%] h-[50vh] w-[30vw] rounded-full bg-blue-600/10 blur-[150px]"
      />
      <motion.div
        animate={{ opacity: [0.2, 0.3, 0.2], x: [0, -20, 0] }}
        transition={{ duration: 22, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        className="absolute -right-[10%] bottom-[10%] h-[50vh] w-[30vw] rounded-full bg-indigo-600/10 blur-[150px]"
      />

      {/* Tiny floating particles */}
      {mounted && (
        <div className="absolute inset-0 pointer-events-none">
          {[...Array(15)].map((_, i) => (
            <motion.div
              key={i}
              initial={{
                opacity: 0,
                y: Math.random() * window.innerHeight,
                x: Math.random() * window.innerWidth,
              }}
              animate={{
                opacity: [0, 0.8, 0],
                y: [null, Math.random() * window.innerHeight - 100],
                x: [null, Math.random() * window.innerWidth + (Math.random() > 0.5 ? 50 : -50)],
              }}
              transition={{
                duration: Math.random() * 10 + 15,
                repeat: Infinity,
                ease: "linear",
                delay: Math.random() * 5,
              }}
              className="absolute h-1 w-1 rounded-full bg-amber-100/40 blur-[1px]"
              style={{
                width: Math.random() * 4 + 1 + "px",
                height: Math.random() * 4 + 1 + "px",
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}
