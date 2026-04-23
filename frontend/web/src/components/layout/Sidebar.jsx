import {
  Home,
  MessageCircle,
  Mic,
  LayoutDashboard,
  Settings,
  ShieldCheck,
  Sparkles,
  Cpu,
  User,
} from "lucide-react";

const menu = [
  { id: "home", label: "Home", icon: Home },
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "chat", label: "Chat", icon: MessageCircle },
  { id: "voice", label: "Voice", icon: Mic },
  { id: "security", label: "Security", icon: ShieldCheck },
  { id: "settings", label: "Settings", icon: Settings },
];

export default function Sidebar({
  activePage = "chat",
  onChangePage,
}) {
  return (
    <aside
      className="
        h-screen
        w-[88px] md:w-[280px] xl:w-[300px]
        shrink-0
        relative overflow-hidden
        border-r border-white/10
        bg-[#08111f]/90
        backdrop-blur-3xl
        flex flex-col
        px-3 py-3 md:px-4 md:py-4
      "
    >
      {/* Background Glow */}
      <div className="absolute -top-10 -left-8 w-36 h-36 bg-cyan-500/10 blur-3xl rounded-full" />
      <div className="absolute bottom-10 -right-8 w-36 h-36 bg-purple-500/10 blur-3xl rounded-full" />

      {/* Scroll Content */}
      <div className="relative z-10 flex-1 min-h-0 flex flex-col">
        {/* PROFILE */}
        <div className="mb-4">
          <div
            className="
              rounded-3xl
              border border-cyan-400/10
              bg-white/[0.03]
              p-3
              relative overflow-hidden
            "
          >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5" />

            <div className="relative flex items-center gap-3">
              {/* Avatar */}
              <div className="relative shrink-0">
                <div
                  className="
                    w-14 h-14 md:w-16 md:h-16
                    rounded-2xl
                    bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-500
                    p-[2px]
                    shadow-[0_0_25px_rgba(34,211,238,0.22)]
                  "
                >
                  <div
                    className="
                      w-full h-full rounded-2xl
                      bg-[#07111f]
                      flex items-center justify-center
                      relative overflow-hidden
                    "
                  >
                    <User
                      size={28}
                      className="text-cyan-200"
                    />

                    <div className="absolute inset-0 bg-cyan-400/10 animate-pulse" />
                  </div>
                </div>

                <span className="absolute -bottom-1 -right-1 w-3.5 h-3.5 rounded-full bg-green-400 border-2 border-[#08111f]" />
              </div>

              {/* Text */}
              <div className="hidden md:block min-w-0">
                <h2 className="text-white font-semibold text-sm">
                  Nilima
                </h2>

                <p className="text-[11px] text-cyan-300">
                  Li Ao Assistant
                </p>

                <p className="text-[11px] text-gray-400 truncate mt-1">
                  Ready for Sadik
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* MENU */}
        <div className="flex-1 min-h-0 overflow-y-auto pr-1 space-y-2 custom-scrollbar">
          {menu.map((item) => {
            const Icon = item.icon;
            const active = activePage === item.id;

            return (
              <button
                key={item.id}
                onClick={() =>
                  onChangePage?.(item.id)
                }
                className={`
                  w-full rounded-2xl
                  border transition-all duration-300
                  ${
                    active
                      ? "border-cyan-300/20 bg-gradient-to-r from-cyan-500/20 to-purple-500/20"
                      : "border-transparent hover:bg-white/[0.04]"
                  }
                `}
              >
                <div className="flex items-center gap-3 px-3 py-3">
                  <div
                    className={`
                      w-11 h-11 rounded-xl
                      flex items-center justify-center
                      ${
                        active
                          ? "bg-white/10 text-cyan-300"
                          : "text-gray-400"
                      }
                    `}
                  >
                    <Icon size={19} />
                  </div>

                  <span
                    className={`
                      hidden md:block text-sm font-medium
                      ${
                        active
                          ? "text-white"
                          : "text-gray-300"
                      }
                    `}
                  >
                    {item.label}
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* STATUS */}
        <div className="pt-4 mt-3">
          <div
            className="
              rounded-3xl
              border border-white/10
              bg-white/[0.03]
              p-3
            "
          >
            <div className="flex items-center gap-3">
              <div
                className="
                  w-11 h-11 rounded-2xl
                  bg-gradient-to-br from-cyan-500/20 to-purple-500/20
                  flex items-center justify-center
                "
              >
                <Cpu
                  size={18}
                  className="text-cyan-300"
                />
              </div>

              <div className="hidden md:block min-w-0">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />

                  <p className="text-xs text-white font-medium">
                    System Online
                  </p>
                </div>

                <p className="text-[11px] text-gray-400 truncate">
                  Li Ao Core Active
                </p>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="hidden md:flex mt-3 px-1 items-center gap-2 text-[11px] text-gray-500">
            <Sparkles size={12} />
            Premium Interface
          </div>
        </div>
      </div>
    </aside>
  );
}