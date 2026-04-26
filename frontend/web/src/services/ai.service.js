import api from "./api";

/* ==================================================
   AI SERVICE
   Chat / Stream / Utility
================================================== */

/* =========================================
   SEND MESSAGE
========================================= */
export const sendMessageToAI = async (
  message,
  options = {}
) => {
  try {
    const payload = {
      message: String(
        message || ""
      ).trim(),

      history:
        options.history || [],

      mode:
        options.mode ||
        "chat",

      provider:
        options.provider ||
        "auto",
    };

    const res =
      await api.post(
        "/chat",
        payload
      );

    return {
      success: true,

      reply:
        res.data?.reply ||
        res.data?.response ||
        "No response",

      provider:
        res.data?.provider ||
        "online",

      raw: res.data,
    };
  } catch (error) {
    throw {
      success: false,
      message:
        error.message ||
        "Unable to send message.",
      status:
        error.status ||
        500,
    };
  }
};

/* =========================================
   STREAM RESPONSE
========================================= */
export const streamAIResponse =
  async (
    message,
    onChunk,
    onDone
  ) => {
    try {
      const base =
        import.meta.env
          .VITE_API_URL ||
        "http://localhost:8000";

      const response =
        await fetch(
          `${base}/chat/stream`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify(
              {
                message,
              }
            ),
          }
        );

      if (!response.ok) {
        throw new Error(
          "Streaming failed."
        );
      }

      const reader =
        response.body.getReader();

      const decoder =
        new TextDecoder(
          "utf-8"
        );

      let done = false;

      while (!done) {
        const {
          value,
          done: finished,
        } =
          await reader.read();

        done = finished;

        if (value) {
          const chunk =
            decoder.decode(
              value,
              {
                stream: true,
              }
            );

          if (onChunk) {
            onChunk(chunk);
          }
        }
      }

      if (onDone) {
        onDone();
      }

      return true;
    } catch (error) {
      throw {
        success: false,
        message:
          error.message ||
          "Stream error.",
      };
    }
  };

/* =========================================
   GET SUGGESTIONS
========================================= */
export const getAISuggestions =
  async () => {
    try {
      const res =
        await api.get(
          "/chat/suggestions"
        );

      return (
        res.data
          ?.suggestions || []
      );
    } catch {
      return [
        "Write code",
        "Explain React",
        "Debug error",
        "Open VS Code",
      ];
    }
  };

/* =========================================
   CLEAR AI MEMORY
========================================= */
export const clearAIMemory =
  async () => {
    try {
      const res =
        await api.post(
          "/chat/clear"
        );

      return res.data;
    } catch (error) {
      throw {
        message:
          "Unable to clear memory.",
      };
    }
  };