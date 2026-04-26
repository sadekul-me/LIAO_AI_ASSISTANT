import { useState, useMemo, useCallback } from "react";

/* ==================================================
   useChat Hook
   Clean / Fast / Scalable
================================================== */

export default function useChat() {
  /* =========================================
     STATE
  ========================================= */
  const [messages, setMessages] = useState([]);
  const [activeChatId, setActiveChatId] =
    useState("default");

  const [isTyping, setIsTyping] =
    useState(false);

  const [searchTerm, setSearchTerm] =
    useState("");

  /* =========================================
     HELPERS
  ========================================= */
  const getTime = () =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

  const createMessage = (
    text,
    isUser = false
  ) => ({
    id:
      Date.now() +
      Math.random(),
    text,
    isUser,
    time: getTime(),
  });

  /* =========================================
     MESSAGE CONTROL
  ========================================= */
  const addMessage = useCallback(
    (text, isUser = false) => {
      if (!text?.trim()) return;

      const newMessage =
        createMessage(
          text.trim(),
          isUser
        );

      setMessages((prev) => [
        ...prev,
        newMessage,
      ]);
    },
    []
  );

  const removeMessage = useCallback(
    (id) => {
      setMessages((prev) =>
        prev.filter(
          (item) =>
            item.id !== id
        )
      );
    },
    []
  );

  const updateMessage = useCallback(
    (id, newText) => {
      setMessages((prev) =>
        prev.map((item) =>
          item.id === id
            ? {
                ...item,
                text: newText,
              }
            : item
        )
      );
    },
    []
  );

  const clearMessages =
    useCallback(() => {
      setMessages([]);
    }, []);

  /* =========================================
     CHAT CONTROL
  ========================================= */
  const newChat = useCallback(() => {
    setMessages([]);
    setActiveChatId(
      "chat_" + Date.now()
    );
  }, []);

  const switchChat =
    useCallback((chatId) => {
      setActiveChatId(chatId);
    }, []);

  /* =========================================
     TYPING
  ========================================= */
  const startTyping =
    useCallback(() => {
      setIsTyping(true);
    }, []);

  const stopTyping =
    useCallback(() => {
      setIsTyping(false);
    }, []);

  /* =========================================
     SEARCH
  ========================================= */
  const filteredMessages =
    useMemo(() => {
      if (!searchTerm.trim())
        return messages;

      const term =
        searchTerm.toLowerCase();

      return messages.filter(
        (item) =>
          item.text
            .toLowerCase()
            .includes(term)
      );
    }, [messages, searchTerm]);

  /* =========================================
     STATS
  ========================================= */
  const totalMessages =
    messages.length;

  const userMessages =
    messages.filter(
      (m) => m.isUser
    ).length;

  const aiMessages =
    messages.filter(
      (m) => !m.isUser
    ).length;

  /* =========================================
     EXPORT
  ========================================= */
  return {
    messages,
    filteredMessages,

    activeChatId,

    isTyping,
    searchTerm,

    totalMessages,
    userMessages,
    aiMessages,

    addMessage,
    removeMessage,
    updateMessage,
    clearMessages,

    newChat,
    switchChat,

    startTyping,
    stopTyping,

    setSearchTerm,
    setMessages,
  };
}