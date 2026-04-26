// context/UIContext.jsx

import { createContext, useState, useCallback } from "react";

export const UIContext = createContext(null);

export const UIProvider = ({ children }) => {
  // 🔹 Sidebar state
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // 🔹 Modal state
  const [modal, setModal] = useState({
    isOpen: false,
    content: null,
  });

  // 🔹 Sidebar controls
  const toggleSidebar = useCallback(() => {
    setIsSidebarOpen((prev) => !prev);
  }, []);

  const openSidebar = useCallback(() => {
    setIsSidebarOpen(true);
  }, []);

  const closeSidebar = useCallback(() => {
    setIsSidebarOpen(false);
  }, []);

  // 🔹 Modal controls
  const openModal = useCallback((content) => {
    setModal({
      isOpen: true,
      content,
    });
  }, []);

  const closeModal = useCallback(() => {
    setModal({
      isOpen: false,
      content: null,
    });
  }, []);

  return (
    <UIContext.Provider
      value={{
        isSidebarOpen,
        toggleSidebar,
        openSidebar,
        closeSidebar,
        modal,
        openModal,
        closeModal,
      }}
    >
      {children}
    </UIContext.Provider>
  );
};