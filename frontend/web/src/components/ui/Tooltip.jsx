// components/ui/Tooltip.jsx

import { useState } from "react";
import clsx from "clsx";

const Tooltip = ({
  children,
  text = "",
  content,
  position = "top", // top | bottom | left | right
  delay = 120,
  disabled = false,
  className = "",
}) => {
  const [visible, setVisible] = useState(false);
  let timer;

  const label = content || text;

  const showTooltip = () => {
    if (disabled || !label) return;

    timer = setTimeout(() => {
      setVisible(true);
    }, delay);
  };

  const hideTooltip = () => {
    clearTimeout(timer);
    setVisible(false);
  };

  const positions = {
    top: `
      bottom-full
      left-1/2
      -translate-x-1/2
      mb-3
    `,
    bottom: `
      top-full
      left-1/2
      -translate-x-1/2
      mt-3
    `,
    left: `
      right-full
      top-1/2
      -translate-y-1/2
      mr-3
    `,
    right: `
      left-full
      top-1/2
      -translate-y-1/2
      ml-3
    `,
  };

  const arrows = {
    top: `
      absolute top-full left-1/2
      -translate-x-1/2
      border-[6px]
      border-transparent
      border-t-black/80
    `,
    bottom: `
      absolute bottom-full left-1/2
      -translate-x-1/2
      border-[6px]
      border-transparent
      border-b-black/80
    `,
    left: `
      absolute left-full top-1/2
      -translate-y-1/2
      border-[6px]
      border-transparent
      border-l-black/80
    `,
    right: `
      absolute right-full top-1/2
      -translate-y-1/2
      border-[6px]
      border-transparent
      border-r-black/80
    `,
  };

  return (
    <div
      className={clsx("relative inline-flex", className)}
      onMouseEnter={showTooltip}
      onMouseLeave={hideTooltip}
      onFocus={showTooltip}
      onBlur={hideTooltip}
    >
      {/* Trigger */}
      {children}

      {/* Tooltip */}
      {visible && (
        <div
          role="tooltip"
          className={clsx(
            `
            absolute z-[999]
            pointer-events-none
            whitespace-nowrap
            px-3 py-1.5
            rounded-xl
            text-[11px] font-medium tracking-wide
            text-white
            bg-black/80
            border border-white/10
            backdrop-blur-xl
            shadow-[0_10px_30px_rgba(0,0,0,.35)]
            animate-in fade-in zoom-in-95 duration-200
            `,
            positions[position]
          )}
        >
          {label}

          {/* Arrow */}
          <span className={clsx(arrows[position])} />
        </div>
      )}
    </div>
  );
};

export default Tooltip;