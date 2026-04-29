import { useState, useEffect, useRef, useCallback } from "react";
import {
  sendMessage as apiSendMessage,
  getTTS,
  getSystemStatus,
} from "../services/api";

/* ==================================================
   useAI Hook - Optimized for Real-time Voice & Chat
================================================== */

export default function useAI() {
  /* =========================================
      STATE
  ========================================= */
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const [isOnline, setIsOnline] = useState(false);
  const [provider, setProvider] = useState("offline");

  const [error, setError] = useState(null);

  const sendingRef = useRef(false);
  const mountedRef = useRef(true);
  const audioRef = useRef(null); // আগের অডিও থামানোর জন্য

  const STORAGE_KEY = "liao_chat_history";
  const HEALTH_INTERVAL = 15000;

  /* =========================================
      HELPERS
  ========================================= */
  const getTime = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  const createMessage = (text, isUser = false) => ({
    id: Date.now() + Math.random(),
    text,
    isUser,
    time: getTime(),
  });

  const safeSetState = (callback) => {
    if (mountedRef.current) callback();
  };

  /* =========================================
      WELCOME / STORAGE
  ========================================= */
  const loadWelcome = useCallback(() => {
    setMessages([createMessage("Hello! I'm LIAO Assistant.", false)]);
  }, []);

  const loadStoredMessages = useCallback(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        loadWelcome();
        return;
      }
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed) && parsed.length > 0) {
        setMessages(parsed);
      } else {
        loadWelcome();
      }
    } catch {
      loadWelcome();
    }
  }, [loadWelcome]);

  const persistMessages = useCallback((data) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (err) {
      console.warn("Storage error:", err);
    }
  }, []);

  /* =========================================
      BACKEND HEALTH
  ========================================= */
  const checkBackendHealth = useCallback(async () => {
    try {
      await getSystemStatus();
      safeSetState(() => setIsOnline(true));
    } catch {
      safeSetState(() => {
        setIsOnline(false);
        setProvider("offline");
      });
    }
  }, []);

  /* =========================================
      INIT & AUTO SAVE
  ========================================= */
  useEffect(() => {
    mountedRef.current = true;
    loadStoredMessages();
    checkBackendHealth();

    const interval = setInterval(checkBackendHealth, HEALTH_INTERVAL);
    return () => {
      mountedRef.current = false;
      clearInterval(interval);
      if (audioRef.current) audioRef.current.pause(); // ক্লিনআপ
    };
  }, [loadStoredMessages, checkBackendHealth]);

  useEffect(() => {
    if (messages.length > 0) persistMessages(messages);
  }, [messages, persistMessages]);

  /* =========================================
      FALLBACK
  ========================================= */
  const fallback = useCallback((text) => {
    const t = text.toLowerCase();
    if (t.includes("hello") || t.includes("hi")) return "Hello.";
    if (t.includes("name")) return "I am LIAO Assistant.";
    if (t.includes("code")) return "Ready for development tasks.";
    if (t.includes("help")) return "Tell me what you need.";
    if (t.includes("time")) return `Current time is ${getTime()}.`;
    return "I'm currently in offline mode, but I can still help with basic tasks.";
  }, []);

  /* =========================================
      TTS (AUDIO PLAYBACK FIX)
  ========================================= */
  const speakText = useCallback(
    async (text) => {
      if (!text || !isOnline) return;

      try {
        const res = await getTTS(text);
        
        // যদি ব্যাকএন্ড থেকে সাকসেস মেসেজ এবং ফাইলের নাম আসে
        if (res && res.success && res.audio_path) {
          // আগের কোনো অডিও বাজতে থাকলে সেটা থামিয়ে দাও
          if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current = null;
          }

          const audioUrl = `http://127.0.0.1:8000/static/${res.audio_path}`;
          const audio = new Audio(audioUrl);
          audioRef.current = audio;
          
          await audio.play();
        }
      } catch (err) {
        console.error("TTS Playback Error:", err);
      }
    },
    [isOnline]
  );

  /* =========================================
      SEND MESSAGE
  ========================================= */
  const sendMessage = useCallback(
    async (text) => {
      const cleanText = String(text || "").trim();
      if (!cleanText || sendingRef.current) return;

      sendingRef.current = true;
      setError(null);
      setIsLoading(true);

      const userMessage = createMessage(cleanText, true);
      setMessages((prev) => [...prev, userMessage]);

      try {
        let reply = "";
        let currentProvider = "offline";

        if (isOnline) {
          try {
            const res = await apiSendMessage(cleanText);
            reply = res?.reply || res?.message || "";
            currentProvider = res?.provider || "online";
          } catch (err) {
            console.warn("API error, falling back to local...");
          }
        }

        if (!reply) {
          reply = fallback(cleanText);
          currentProvider = "offline";
        }

        const botMessage = createMessage(reply, false);

        safeSetState(() => {
          setMessages((prev) => [...prev, botMessage]);
          setProvider(currentProvider);
        });

        // রিপ্লাই আসার সাথে সাথে লিয়াও কথা বলবে
        speakText(reply);

      } catch (err) {
        safeSetState(() => {
          setError("Connection lost.");
          setMessages((prev) => [...prev, createMessage("Something went wrong.", false)]);
        });
      } finally {
        safeSetState(() => setIsLoading(false));
        sendingRef.current = false;
      }
    },
    [isOnline, fallback, speakText]
  );

  /* =========================================
      CHAT CONTROL
  ========================================= */
  const clearChat = useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {}
    setMessages([createMessage("Conversation cleared.", false)]);
  }, []);

  const removeMessage = useCallback((id) => {
    setMessages((prev) => prev.filter((item) => item.id !== id));
  }, []);

  /* =========================================
      VOICE STATES
  ========================================= */
  const startListening = useCallback(() => setIsListening(true), []);
  const stopListening = useCallback(() => setIsListening(false), []);
  const toggleListening = useCallback(() => setIsListening((prev) => !prev), []);

  /* =========================================
      EXPORT
  ========================================= */
  return {
    messages,
    sendMessage,
    clearChat,
    removeMessage,
    isLoading,
    error,
    isListening,
    startListening,
    stopListening,
    toggleListening,
    isOnline,
    provider,
    speakText,
    checkBackendHealth,
  };
}