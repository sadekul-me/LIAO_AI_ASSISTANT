import { useState, useEffect, useRef, useCallback } from "react";
import {
  sendMessage as apiSendMessage,
  getTTS,
  getSystemStatus,
} from "../services/api";

/* ==================================================
   useAI Hook
   Clean / Scalable / Production Ready
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
     WELCOME
  ========================================= */
  const loadWelcome = useCallback(() => {
    setMessages([
      createMessage("Hello! I'm LIAO Assistant.", false),
    ]);
  }, []);

  /* =========================================
     LOAD CHAT
  ========================================= */
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

  /* =========================================
     SAVE CHAT
  ========================================= */
  const persistMessages = useCallback((data) => {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(data)
      );
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

      safeSetState(() => {
        setIsOnline(true);
      });
    } catch {
      safeSetState(() => {
        setIsOnline(false);
        setProvider("offline");
      });
    }
  }, []);

  /* =========================================
     INIT
  ========================================= */
  useEffect(() => {
    mountedRef.current = true;

    loadStoredMessages();
    checkBackendHealth();

    const interval = setInterval(() => {
      checkBackendHealth();
    }, HEALTH_INTERVAL);

    return () => {
      mountedRef.current = false;
      clearInterval(interval);
    };
  }, [loadStoredMessages, checkBackendHealth]);

  /* =========================================
     AUTO SAVE
  ========================================= */
  useEffect(() => {
    if (messages.length > 0) {
      persistMessages(messages);
    }
  }, [messages, persistMessages]);

  /* =========================================
     FALLBACK RESPONSE
  ========================================= */
  const fallback = useCallback((text) => {
    const t = text.toLowerCase();

    if (t.includes("hello") || t.includes("hi"))
      return "Hello.";

    if (t.includes("name"))
      return "I am LIAO Assistant.";

    if (t.includes("code"))
      return "Ready for development tasks.";

    if (t.includes("help"))
      return "Tell me what you need.";

    if (t.includes("time"))
      return `Current time is ${getTime()}.`;

    return "Offline mode active.";
  }, []);

  /* =========================================
     TTS
  ========================================= */
  const speakText = useCallback(
    async (text) => {
      if (!text || !isOnline) return;

      try {
        await getTTS(text);
      } catch (err) {
        console.warn("TTS error:", err);
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

      if (!cleanText) return;
      if (sendingRef.current) return;

      sendingRef.current = true;
      setError(null);
      setIsLoading(true);

      const userMessage = createMessage(
        cleanText,
        true
      );

      setMessages((prev) => [...prev, userMessage]);

      try {
        let reply = "";
        let currentProvider = "offline";

        if (isOnline) {
          try {
            const res = await apiSendMessage(
              cleanText
            );

            reply =
              res?.reply ||
              res?.message ||
              "";

            currentProvider =
              res?.provider ||
              "online";
          } catch (err) {
            console.warn(
              "API error:",
              err
            );
          }
        }

        if (!reply) {
          reply = fallback(cleanText);
          currentProvider = "offline";
        }

        const botMessage = createMessage(
          reply,
          false
        );

        safeSetState(() => {
          setMessages((prev) => [
            ...prev,
            botMessage,
          ]);

          setProvider(currentProvider);
        });

        speakText(reply);
      } catch (err) {
        safeSetState(() => {
          setError(
            "Unable to process request."
          );

          setMessages((prev) => [
            ...prev,
            createMessage(
              "Something went wrong.",
              false
            ),
          ]);
        });
      } finally {
        safeSetState(() => {
          setIsLoading(false);
        });

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

    setMessages([
      createMessage(
        "Conversation cleared.",
        false
      ),
    ]);
  }, []);

  const removeMessage = useCallback((id) => {
    setMessages((prev) =>
      prev.filter((item) => item.id !== id)
    );
  }, []);

  /* =========================================
     VOICE
  ========================================= */
  const startListening = useCallback(() => {
    setIsListening(true);
  }, []);

  const stopListening = useCallback(() => {
    setIsListening(false);
  }, []);

  const toggleListening = useCallback(() => {
    setIsListening((prev) => !prev);
  }, []);

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