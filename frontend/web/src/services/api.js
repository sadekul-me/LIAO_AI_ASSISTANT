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
    const token =
      localStorage.getItem(
        "liao_auth_token"
      );

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
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
    const status =
      error?.response?.status;

    const message =
      error?.response?.data
        ?.message ||
      error.message ||
      "Request failed";

    /* Unauthorized */
    if (status === 401) {
      localStorage.removeItem(
        "liao_auth_token"
      );
      localStorage.removeItem(
        "liao_auth_user"
      );
    }

    /* Optional global logging */
    console.error(
      "API Error:",
      status,
      message
    );

    return Promise.reject({
      status,
      message,
      raw: error,
    });
  }
);

/* ==================================================
   HEALTH CHECK
================================================== */

export const pingServer =
  async () => {
    const res =
      await api.get("/health");

    return res.data;
  };

/* ==================================================
   EXPORT
================================================== */

export default api;