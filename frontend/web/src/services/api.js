import axios from "axios";

/* ==================================================
   API CONFIG
================================================== */
const BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";

/* ==================================================
   AXIOS INSTANCE
================================================== */
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

/* ==================================================
   REQUEST INTERCEPTOR
================================================== */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("liao_auth_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/* ==================================================
   RESPONSE INTERCEPTOR
================================================== */
api.interceptors.response.use(
  (response) => response,

  (error) => {
    const status = error?.response?.status;
    const message =
      error?.response?.data?.message ||
      error.message ||
      "Request failed";

    /* Unauthorized */
    if (status === 401) {
      localStorage.removeItem("liao_auth_token");
      localStorage.removeItem("liao_auth_user");
    }

    /* Optional global logging */
    console.error("API Error:", status, message);

    return Promise.reject({
      status,
      message,
      raw: error,
    });
  }
);

/* ==================================================
   VOICE SERVICES (STT & TTS)
================================================== */

/**
 * Speech To Text: Sends audio file to backend
 * @param {Blob} audioFile - The recorded audio blob
 */
export const speechToText = async (audioFile) => {
  const formData = new FormData();
  // Key must be 'file' as defined in FastAPI backend
  formData.append("file", audioFile, "recording.wav");

  const res = await api.post("/voice/stt", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};

/**
 * Text To Speech: Sends text to get audio path
 * @param {string} text - The response text from AI
 */
export const textToSpeech = async (text) => {
  const res = await api.post("/voice/tts", { text });
  return res.data;
};

/* ==================================================
   HEALTH CHECK
================================================== */
export const pingServer = async () => {
  const res = await api.get("/health");
  return res.data;
};

/* ==================================================
   EXPORT
================================================== */
export default api;