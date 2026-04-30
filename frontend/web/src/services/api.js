import axios from "axios";

/* ==================================================
   BASE CONFIG
================================================== */
const BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

/* ==================================================
   AXIOS INSTANCE
================================================== */
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  withCredentials: false,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

/* ==================================================
   HELPERS
================================================== */
const getToken = () => {
  return localStorage.getItem("liao_auth_token");
};

const clearAuth = () => {
  localStorage.removeItem("liao_auth_token");
  localStorage.removeItem("liao_auth_user");
};

const buildError = (error) => {
  const status = error?.response?.status || 500;

  const message =
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.message ||
    "Request failed";

  return {
    status,
    message,
    raw: error,
  };
};

/* ==================================================
   REQUEST INTERCEPTOR
================================================== */
api.interceptors.request.use(
  (config) => {
    const token = getToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(buildError(error))
);

/* ==================================================
   RESPONSE INTERCEPTOR
================================================== */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;

    if (status === 401) {
      clearAuth();
    }

    const formatted = buildError(error);

    console.error("API ERROR:", formatted.status, formatted.message);

    return Promise.reject(formatted);
  }
);

/* ==================================================
   GENERIC REQUEST METHODS
================================================== */
export const getRequest = async (url, config = {}) => {
  const res = await api.get(url, config);
  return res.data;
};

export const postRequest = async (url, data = {}, config = {}) => {
  const res = await api.post(url, data, config);
  return res.data;
};

export const putRequest = async (url, data = {}, config = {}) => {
  const res = await api.put(url, data, config);
  return res.data;
};

export const deleteRequest = async (url, config = {}) => {
  const res = await api.delete(url, config);
  return res.data;
};

/* ==================================================
   CHAT SERVICES
================================================== */
export const sendChatMessage = async (
  message,
  sessionId = "frontend_user"
) => {
  return await postRequest("/chat", {
    message,
    session_id: sessionId,
  });
};

export const detectIntent = async (
  message,
  sessionId = "frontend_user"
) => {
  return await postRequest("/chat/intent", {
    message,
    session_id: sessionId,
  });
};

export const getChatStatus = async () => {
  return await getRequest("/chat");
};

export const pingChat = async () => {
  return await getRequest("/chat/ping");
};

/* ==================================================
   VOICE SERVICES
================================================== */

/* Speech To Text */
export const speechToText = async (audioBlob) => {
  const formData = new FormData();

  formData.append(
    "file",
    audioBlob,
    "liao_recording.wav"
  );

  const res = await api.post(
    "/voice/stt",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return res.data;
};

/* Text To Speech */
export const textToSpeech = async (text) => {
  return await postRequest("/voice/tts", {
    text,
  });
};

export const getVoiceStatus = async () => {
  return await getRequest("/voice/status");
};

/* Build Audio URL */
export const getAudioUrl = (fileName) => {
  if (!fileName) return "";

  const cleanName = fileName
    .split("\\")
    .pop()
    .split("/")
    .pop();

  return `${BASE_URL}/static/${cleanName}?t=${Date.now()}`;
};

/* ==================================================
   SYSTEM / HEALTH
================================================== */
export const pingServer = async () => {
  try {
    return await getRequest("/health");
  } catch {
    return {
      status: "offline",
    };
  }
};

export const checkBackend = async () => {
  try {
    await getRequest("/chat/ping");
    return true;
  } catch {
    return false;
  }
};

/* ==================================================
   AUTH PLACEHOLDER
================================================== */
export const logoutUser = () => {
  clearAuth();
};

/* ==================================================
   EXPORT
================================================== */
export default api;