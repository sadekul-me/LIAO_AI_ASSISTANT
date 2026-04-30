import React, { createContext, useContext, useState } from "react";
import { sendMessageToAI } from "../services/ai.service";

export const AIContext = createContext();

export const AIProvider = ({ children }) => {
  const [messages, setMessages] = useState([
    {
      id: crypto.randomUUID(),
      role: "ai",
      content: "Hello Sadekul 👋 I'm LIAO AI. How can I assist you today?",
      time: formatTime(),
      status: "done",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [currentModel, setCurrentModel] = useState("LIAO-v3-Turbo");

  /* =========================
     SEND MESSAGE (CLEAN)
  ========================= */
  const sendMessage = async (text) => {
    const cleanText = text?.trim();
    if (!cleanText || isLoading) return;

    // USER MESSAGE
    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: cleanText,
      time: formatTime(),
      status: "done",
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const res = await sendMessageToAI(cleanText);

      const reply =
        typeof res === "string"
          ? res
          : res?.reply || res?.message || "No response";

      setIsOnline(true);

      // AI RESPONSE (DIRECT UPDATE, NO "Thinking" MESSAGE)
      const aiMessage = {
        id: crypto.randomUUID(),
        role: "ai",
        content: reply,
        time: formatTime(),
        status: "done",
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setIsOnline(false);

      const errorMessage = {
        id: crypto.randomUUID(),
        role: "ai",
        content: "AI is currently unavailable 😓",
        time: formatTime(),
        status: "error",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  /* =========================
     CLEAR CHAT
  ========================= */
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

/* =========================
   HELPERS
========================= */
const formatTime = () =>
  new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

export const useAI = () => {
  const context = useContext(AIContext);

  if (!context) {
    throw new Error("useAI must be used within AIProvider");
  }

  return context;
};