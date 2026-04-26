// components/ui/GlassCard.jsx

import clsx from "clsx";

const GlassCard = ({
  children,
  className = "",
  hover = true,
  padding = "p-4",
}) => {
  return (
    <div
      className={clsx(
        "relative rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-lg",
        hover && "transition hover:bg-white/10 hover:shadow-xl",
        padding,
        className
      )}
    >
      {/* 🔹 Glow effect */}
      <div className="pointer-events-none absolute inset-0 rounded-2xl bg-gradient-to-br from-white/5 to-transparent opacity-40" />

      {/* 🔹 Content */}
      <div className="relative z-10">{children}</div>
    </div>
  );
};

export default GlassCard;