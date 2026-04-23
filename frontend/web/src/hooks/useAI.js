import { useState, useEffect, useRef } from "react";
import { sendMessage as apiSendMessage, getTTS, getSystemStatus } from "../services/api";

/* ==================================================
   🤖 useAI Hook
================================================== */
export default function useAI() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const [provider, setProvider] = useState("offline");

  const sendingRef = useRef(false);

  const STORAGE_KEY = "liao_chat_history";

  /* =========================
     INIT
  ========================= */
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);

    if (saved) {
      try {
        setMessages(JSON.parse(saved));
      } catch {
        loadWelcome();
      }
    } else {
      loadWelcome();
    }

    checkBackendHealth();
  }, []);

  /* =========================
     SAVE CHAT
  ========================= */
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(messages)
      );
    }
  }, [messages]);

  /* =========================
     WELCOME
  ========================= */
  const loadWelcome = () => {
    setMessages([
      {
        text: "Hello! I'm LIAO AI Assistant.",
        isUser: false,
        time: getTime(),
      },
    ]);
  };

  const getTime = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  /* =========================
     HEALTH CHECK
  ========================= */
  const checkBackendHealth = async () => {
    try {
      await getSystemStatus();
      setIsOnline(true);
    } catch {
      setIsOnline(false);
    }
  };

  /* =========================
     SEND MESSAGE
  ========================= */
  const sendMessage = async (text) => {
    const cleanText = (text || "").trim();
    if (!cleanText || sendingRef.current) return;

    sendingRef.current = true;

    const userMsg = {
      text: cleanText,
      isUser: true,
      time: getTime(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      let replyText = "";
      let backendProvider = "offline";

      if (isOnline) {
        try {
          const res = await apiSendMessage(cleanText);

          replyText = res?.reply || "";
          backendProvider = res?.provider || "online";
        } catch (err) {
          console.warn("Backend error:", err.message);
        }
      }

      if (!replyText) {
        replyText = fallback(cleanText);
      }

      const aiMsg = {
        text: replyText,
        isUser: false,
        time: getTime(),
      };

      setMessages((prev) => [...prev, aiMsg]);
      setProvider(backendProvider);

      speakText(replyText);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: "Error occurred",
          isUser: false,
          time: getTime(),
        },
      ]);
    }

    setIsLoading(false);
    sendingRef.current = false;
  };

  /* =========================
     TTS
  ========================= */
  const speakText = async (text) => {
    try {
      if (!isOnline) return;
      await getTTS(text);
    } catch (e) {
      console.warn("TTS failed:", e.message);
    }
  };

  /* =========================
     CLEAR CHAT
  ========================= */
  const clearChat = () => {
    localStorage.removeItem(STORAGE_KEY);

    setMessages([
      {
        text: "Chat cleared.",
        isUser: false,
        time: getTime(),
      },
    ]);
  };

  /* =========================
     TOGGLE
  ========================= */
  const toggleListening = () => {
    setIsListening((p) => !p);
  };

  /* =========================
     FALLBACK AI
  ========================= */
  const fallback = (text) => {
    const t = text.toLowerCase();

    if (t.includes("hello")) return "Hey 👋";
    if (t.includes("code")) return "Coding help ready 💻";
    if (t.includes("name")) return "I am LIAO AI Assistant";

    return "Offline mode active 🚀";
  };

  return {
    messages,
    sendMessage,
    clearChat,

    isLoading,
    isListening,
    toggleListening,

    isOnline,
    provider,

    speakText,
    checkBackendHealth,
  };
}