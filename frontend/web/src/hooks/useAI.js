import { useState, useEffect, useRef } from "react";
import axios from "axios";

/* ==================================================
   🔧 CONFIG
================================================== */
const BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const CHAT_API = `${BASE_URL}/chat/`;
const HEALTH_API = `${BASE_URL}/`;
const TTS_API = `${BASE_URL}/voice/tts`;

const STORAGE_KEY = "liao_chat_history";

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

  /* ==================================================
     🚀 LOAD CHAT HISTORY
  ================================================== */
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

  /* ==================================================
     💾 SAVE HISTORY
  ================================================== */
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(messages)
      );
    }
  }, [messages]);

  /* ==================================================
     👋 WELCOME MESSAGE
  ================================================== */
  const loadWelcome = () => {
    setMessages([
      {
        text: "Hello! I'm LIAO AI Assistant. How can I help you?",
        isUser: false,
        time: getTime(),
      },
    ]);
  };

  /* ==================================================
     🕒 TIME FORMAT
  ================================================== */
  const getTime = () => {
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  /* ==================================================
     🌐 BACKEND HEALTH CHECK
  ================================================== */
  const checkBackendHealth = async () => {
    try {
      await axios.get(HEALTH_API, {
        timeout: 3000,
      });

      setIsOnline(true);
    } catch {
      setIsOnline(false);
    }
  };

  /* ==================================================
     💬 SEND MESSAGE
  ================================================== */
  const sendMessage = async (text) => {
    const cleanText = text.trim();

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
          const res = await axios.post(
            CHAT_API,
            {
              message: cleanText,
              context: "",
            },
            {
              timeout: 30000,
            }
          );

          replyText =
            res?.data?.reply ||
            "";

          backendProvider =
            res?.data?.provider ||
            "online";

        } catch (error) {
          console.warn(
            "Backend chat failed:",
            error.message
          );
        }
      }

      /* =========================
         🤖 FALLBACK MODE
      ========================= */
      if (!replyText) {
        replyText = generateFallback(cleanText);
        backendProvider = "offline";
      }

      await delay(500);

      const aiMsg = {
        text: replyText,
        isUser: false,
        time: getTime(),
      };

      setMessages((prev) => [...prev, aiMsg]);
      setProvider(backendProvider);

      /* =========================
         🔊 AUTO SPEAK
      ========================= */
      speakText(replyText);

    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: "⚠️ Something went wrong.",
          isUser: false,
          time: getTime(),
        },
      ]);
    }

    setIsLoading(false);
    sendingRef.current = false;
  };

  /* ==================================================
     🔊 TEXT TO SPEECH
  ================================================== */
  const speakText = async (text) => {
    try {
      if (!isOnline) return;

      await axios.post(TTS_API, {
        text,
      });
    } catch (error) {
      console.warn(
        "TTS failed:",
        error.message
      );
    }
  };

  /* ==================================================
     🎤 VOICE TOGGLE
  ================================================== */
  const toggleListening = () => {
    setIsListening((prev) => !prev);
  };

  /* ==================================================
     🧹 CLEAR CHAT
  ================================================== */
  const clearChat = () => {
    localStorage.removeItem(STORAGE_KEY);

    setMessages([
      {
        text: "Chat cleared. How can I help again?",
        isUser: false,
        time: getTime(),
      },
    ]);
  };

  /* ==================================================
     🤖 OFFLINE FALLBACK AI
  ================================================== */
  const generateFallback = (text) => {
    const lower = text.toLowerCase();

    if (
      lower.includes("hello") ||
      lower.includes("hi")
    ) {
      return "Hey 👋 How can I help you today?";
    }

    if (
      lower.includes("code")
    ) {
      return "I can help you write and debug code 💻";
    }

    if (
      lower.includes("open")
    ) {
      return "App automation feature is available ⚡";
    }

    if (
      lower.includes("ai")
    ) {
      return "AI system is running in offline demo mode 🤖";
    }

    if (
      lower.includes("name")
    ) {
      return "My name is LIAO AI Assistant.";
    }

    return "I'm running in offline mode. Connect backend for full intelligence 🚀";
  };

  /* ==================================================
     ⏱️ DELAY
  ================================================== */
  const delay = (ms) =>
    new Promise((resolve) =>
      setTimeout(resolve, ms)
    );

  /* ==================================================
     📦 RETURN
  ================================================== */
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