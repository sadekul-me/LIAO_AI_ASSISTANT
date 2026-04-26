// components/ai/Avatar.jsx

import { Bot, User, Sparkles } from "lucide-react";
import clsx from "clsx";

const Avatar = ({
  role = "ai", // ai | user
  size = "md", // sm | md | lg | xl
  src = "",
  name = "",
  online = true,
  className = "",
}) => {
  const sizes = {
    sm: {
      box: "w-8 h-8",
      icon: 14,
      dot: "w-2 h-2",
    },
    md: {
      box: "w-10 h-10",
      icon: 16,
      dot: "w-2.5 h-2.5",
    },
    lg: {
      box: "w-12 h-12",
      icon: 18,
      dot: "w-3 h-3",
    },
    xl: {
      box: "w-14 h-14",
      icon: 20,
      dot: "w-3.5 h-3.5",
    },
  };

  const current = sizes[size] || sizes.md;
  const isAI = role === "ai";

  const initials = name
    ? name
        .split(" ")
        .map((item) => item[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "U";

  return (
    <div className={clsx("relative shrink-0", className)}>
      {/* Glow */}
      <div
        className={clsx(
          `
          absolute inset-0
          rounded-2xl
          blur-xl
          opacity-70
          `,
          isAI
            ? "bg-cyan-500/25"
            : "bg-pink-500/20"
        )}
      />

      {/* Main Avatar */}
      <div
        className={clsx(
          `
          relative
          overflow-hidden
          rounded-2xl
          flex items-center justify-center
          border border-white/10
          backdrop-blur-xl
          shadow-[0_10px_25px_rgba(0,0,0,.25)]
          `,
          current.box,
          isAI
            ? `
              bg-gradient-to-br
              from-cyan-400
              via-blue-500
              to-purple-600
            `
            : `
              bg-gradient-to-br
              from-pink-500
              via-orange-400
              to-yellow-400
            `
        )}
      >
        {/* Shine Overlay */}
        <div
          className="
            absolute inset-0
            bg-gradient-to-br
            from-white/20
            via-transparent
            to-transparent
          "
        />

        {/* AI Avatar */}
        {isAI && (
          <>
            <Bot
              size={current.icon}
              className="relative text-white"
            />

            <Sparkles
              size={10}
              className="
                absolute top-1 right-1
                text-cyan-100
                animate-pulse
              "
            />
          </>
        )}

        {/* User Avatar */}
        {!isAI &&
          (src ? (
            <img
              src={src}
              alt="avatar"
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="relative flex items-center justify-center w-full h-full">
              <User
                size={current.icon}
                className="absolute text-white/90"
              />

              <span className="relative text-white text-xs font-semibold">
                {initials}
              </span>
            </div>
          ))}
      </div>

      {/* Online Status */}
      {online && (
        <span
          className={clsx(
            `
            absolute -bottom-0.5 -right-0.5
            rounded-full
            bg-green-400
            border-2 border-[#081122]
            animate-pulse
            `,
            current.dot
          )}
        />
      )}
    </div>
  );
};

export default Avatar;