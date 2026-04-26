import api from "./api";

/* ==================================================
   SYSTEM SERVICE
   Health / Status / Commands / Info
================================================== */

/* =========================================
   HEALTH CHECK
========================================= */
export const getSystemStatus =
  async () => {
    try {
      const res =
        await api.get(
          "/health"
        );

      return {
        success: true,
        online: true,
        data: res.data,
      };
    } catch (error) {
      return {
        success: false,
        online: false,
        message:
          error.message ||
          "Server offline.",
      };
    }
  };

/* =========================================
   SYSTEM INFO
========================================= */
export const getSystemInfo =
  async () => {
    try {
      const res =
        await api.get(
          "/system/info"
        );

      return {
        success: true,
        data: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          error.message ||
          "Unable to fetch system info.",
      };
    }
  };

/* =========================================
   EXECUTE COMMAND
========================================= */
export const runSystemCommand =
  async (
    command,
    payload = {}
  ) => {
    try {
      const res =
        await api.post(
          "/system/command",
          {
            command,
            ...payload,
          }
        );

      return {
        success: true,
        data: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          error.message ||
          "Command failed.",
      };
    }
  };

/* =========================================
   OPEN APP
========================================= */
export const openApplication =
  async (appName) => {
    try {
      const res =
        await api.post(
          "/system/open-app",
          {
            app: appName,
          }
        );

      return {
        success: true,
        data: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          "Unable to open application.",
      };
    }
  };

/* =========================================
   OPEN WEBSITE
========================================= */
export const openWebsite =
  async (url) => {
    try {
      const res =
        await api.post(
          "/system/open-url",
          {
            url,
          }
        );

      return {
        success: true,
        data: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          "Unable to open website.",
      };
    }
  };

/* =========================================
   RESTART AI ENGINE
========================================= */
export const restartEngine =
  async () => {
    try {
      const res =
        await api.post(
          "/system/restart"
        );

      return {
        success: true,
        data: res.data,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          "Restart failed.",
      };
    }
  };

/* =========================================
   GET LOGS
========================================= */
export const getSystemLogs =
  async () => {
    try {
      const res =
        await api.get(
          "/system/logs"
        );

      return {
        success: true,
        logs:
          res.data?.logs ||
          [],
      };
    } catch (error) {
      throw {
        success: false,
        message:
          "Unable to load logs.",
      };
    }
  };