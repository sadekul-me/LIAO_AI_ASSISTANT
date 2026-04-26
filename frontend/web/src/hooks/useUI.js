import { useState, useEffect, useCallback } from "react";

/* ==================================================
   useUI Hook
   Clean / Premium / App Control
================================================== */

export default function useUI() {
  /* =========================================
     STATE
  ========================================= */
  const [theme, setTheme] =
    useState("dark");

  const [sidebarOpen, setSidebarOpen] =
    useState(true);

  const [settingsOpen, setSettingsOpen] =
    useState(false);

  const [profileOpen, setProfileOpen] =
    useState(false);

  const [commandPaletteOpen, setCommandPaletteOpen] =
    useState(false);

  const [notifications, setNotifications] =
    useState([]);

  const [isMobile, setIsMobile] =
    useState(false);

  const [windowWidth, setWindowWidth] =
    useState(window.innerWidth);

  const STORAGE_THEME = "liao_theme";

  /* =========================================
     INIT
  ========================================= */
  useEffect(() => {
    const savedTheme =
      localStorage.getItem(STORAGE_THEME);

    if (savedTheme) {
      setTheme(savedTheme);
    }

    handleResize();

    window.addEventListener(
      "resize",
      handleResize
    );

    return () =>
      window.removeEventListener(
        "resize",
        handleResize
      );
  }, []);

  /* =========================================
     THEME APPLY
  ========================================= */
  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      theme
    );

    localStorage.setItem(
      STORAGE_THEME,
      theme
    );
  }, [theme]);

  /* =========================================
     RESIZE
  ========================================= */
  const handleResize =
    useCallback(() => {
      const width =
        window.innerWidth;

      setWindowWidth(width);
      setIsMobile(width < 768);

      if (width < 768) {
        setSidebarOpen(false);
      }
    }, []);

  /* =========================================
     THEME
  ========================================= */
  const toggleTheme =
    useCallback(() => {
      setTheme((prev) =>
        prev === "dark"
          ? "light"
          : "dark"
      );
    }, []);

  const setDarkTheme =
    useCallback(() => {
      setTheme("dark");
    }, []);

  const setLightTheme =
    useCallback(() => {
      setTheme("light");
    }, []);

  /* =========================================
     SIDEBAR
  ========================================= */
  const openSidebar =
    useCallback(() => {
      setSidebarOpen(true);
    }, []);

  const closeSidebar =
    useCallback(() => {
      setSidebarOpen(false);
    }, []);

  const toggleSidebar =
    useCallback(() => {
      setSidebarOpen((prev) => !prev);
    }, []);

  /* =========================================
     SETTINGS
  ========================================= */
  const openSettings =
    useCallback(() => {
      setSettingsOpen(true);
    }, []);

  const closeSettings =
    useCallback(() => {
      setSettingsOpen(false);
    }, []);

  const toggleSettings =
    useCallback(() => {
      setSettingsOpen(
        (prev) => !prev
      );
    }, []);

  /* =========================================
     PROFILE
  ========================================= */
  const openProfile =
    useCallback(() => {
      setProfileOpen(true);
    }, []);

  const closeProfile =
    useCallback(() => {
      setProfileOpen(false);
    }, []);

  const toggleProfile =
    useCallback(() => {
      setProfileOpen(
        (prev) => !prev
      );
    }, []);

  /* =========================================
     COMMAND PALETTE
  ========================================= */
  const openCommandPalette =
    useCallback(() => {
      setCommandPaletteOpen(true);
    }, []);

  const closeCommandPalette =
    useCallback(() => {
      setCommandPaletteOpen(false);
    }, []);

  const toggleCommandPalette =
    useCallback(() => {
      setCommandPaletteOpen(
        (prev) => !prev
      );
    }, []);

  /* =========================================
     NOTIFICATIONS
  ========================================= */
  const addNotification =
    useCallback(
      (
        text,
        type = "info"
      ) => {
        const item = {
          id:
            Date.now() +
            Math.random(),
          text,
          type,
        };

        setNotifications(
          (prev) => [
            ...prev,
            item,
          ]
        );

        setTimeout(() => {
          removeNotification(
            item.id
          );
        }, 3500);
      },
      []
    );

  const removeNotification =
    useCallback((id) => {
      setNotifications(
        (prev) =>
          prev.filter(
            (item) =>
              item.id !== id
          )
      );
    }, []);

  const clearNotifications =
    useCallback(() => {
      setNotifications([]);
    }, []);

  /* =========================================
     CLOSE ALL PANELS
  ========================================= */
  const closeAllPanels =
    useCallback(() => {
      setSettingsOpen(false);
      setProfileOpen(false);
      setCommandPaletteOpen(false);
    }, []);

  /* =========================================
     EXPORT
  ========================================= */
  return {
    theme,
    isMobile,
    windowWidth,

    sidebarOpen,
    settingsOpen,
    profileOpen,
    commandPaletteOpen,

    notifications,

    toggleTheme,
    setDarkTheme,
    setLightTheme,

    openSidebar,
    closeSidebar,
    toggleSidebar,

    openSettings,
    closeSettings,
    toggleSettings,

    openProfile,
    closeProfile,
    toggleProfile,

    openCommandPalette,
    closeCommandPalette,
    toggleCommandPalette,

    addNotification,
    removeNotification,
    clearNotifications,

    closeAllPanels,
  };
}