import axios from "axios";

/* =========================
   BASE URL
========================= */
const BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

/* =========================
   CHAT API
========================= */
export const sendMessage = async (message, context = "") => {
  const res = await axios.post(`${BASE_URL}/chat/`, {
    message,
    context,
  });

  return res.data;
};

/* =========================
   TTS API
========================= */
export const getTTS = async (text) => {
  const res = await axios.post(`${BASE_URL}/voice/tts`, {
    text,
  });

  return res.data;
};

/* =========================
   SYSTEM STATUS
========================= */
export const getSystemStatus = async () => {
  const res = await axios.get(`${BASE_URL}/system/status`);
  return res.data;
};