import React, {
  createContext,
  useContext,
  useState,
} from "react";

import { sendMessageToAI } from "../services/ai.service";

export const AIContext = createContext();

/* =========================================
   PROVIDER
========================================= */
export const AIProvider = ({ children }) => {
  const [messages, setMessages] = useState([
    {
      id: crypto.randomUUID(),
      role: "ai",
      content:
        "Hello Sadekul 👋\nI'm LIAO AI. How can I assist you today?",
      time: formatTime(),
      status: "done",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [currentModel, setCurrentModel] =
    useState("LIAO-v3-Turbo");

  /* =========================================
     SEND MESSAGE
  ========================================= */
  const sendMessage = async (text) => {
    const cleanText = text?.trim();

    if (!cleanText || isLoading) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: cleanText,
      time: formatTime(),
      status: "done",
    };

    setMessages((prev) => [...prev, userMessage]);

    const tempId = crypto.randomUUID();

    setMessages((prev) => [
      ...prev,
      {
        id: tempId,
        role: "ai",
        content: "Thinking...",
        time: formatTime(),
        status: "typing",
      },
    ]);

    setIsLoading(true);

    try {
      const res = await sendMessageToAI(cleanText);

      const reply =
        typeof res === "string"
          ? res
          : res?.reply || res?.message || "No response";

      // ✅ SUCCESS → ONLINE
      setIsOnline(true);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === tempId
            ? {
                ...msg,
                content: reply,
                status: "done",
                time: formatTime(),
              }
            : msg
        )
      );
    } catch (err) {
      // ❌ ERROR → OFFLINE
      setIsOnline(false);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === tempId
            ? {
                ...msg,
                content:
                  "AI is currently unavailable 😓",
                status: "error",
                time: formatTime(),
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  /* =========================================
     CLEAR CHAT
  ========================================= */
  const clearChat = () => {
    setMessages([
      {
        id: crypto.randomUUID(),
        role: "ai",
        content: "Chat cleared. Ready again 🚀",
        time: formatTime(),
        status: "done",
      },
    ]);
  };

  /* =========================================
     PROVIDER VALUE
  ========================================= */
  return (
    <AIContext.Provider
      value={{
        messages,
        sendMessage,
        isLoading,
        isOnline,
        currentModel,
        setCurrentModel,
        clearChat,
      }}
    >
      {children}
    </AIContext.Provider>
  );
};

/* =========================================
   HELPERS
========================================= */
const formatTime = () =>
  new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

/* =========================================
   HOOK
========================================= */
export const useAI = () => {
  const context = useContext(AIContext);

  if (!context) {
    throw new Error("useAI must be used within AIProvider");
  }

  return context;
};