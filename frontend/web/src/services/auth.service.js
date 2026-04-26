import api from "./api";

/* ==================================================
   AUTH SERVICE
   Login / Register / Session / Profile
================================================== */

const TOKEN_KEY = "liao_auth_token";
const USER_KEY = "liao_auth_user";

/* =========================================
   HELPERS
========================================= */
const saveSession = (
  token,
  user
) => {
  localStorage.setItem(
    TOKEN_KEY,
    token
  );

  localStorage.setItem(
    USER_KEY,
    JSON.stringify(user)
  );
};

const clearSession =
  () => {
    localStorage.removeItem(
      TOKEN_KEY
    );

    localStorage.removeItem(
      USER_KEY
    );
  };

export const getToken =
  () =>
    localStorage.getItem(
      TOKEN_KEY
    ) || "";

export const getUser =
  () => {
    try {
      const raw =
        localStorage.getItem(
          USER_KEY
        );

      return raw
        ? JSON.parse(raw)
        : null;
    } catch {
      return null;
    }
  };

export const isAuthenticated =
  () => !!getToken();

/* =========================================
   LOGIN
========================================= */
export const loginUser =
  async ({
    email,
    password,
  }) => {
    try {
      const res =
        await api.post(
          "/auth/login",
          {
            email:
              email.trim(),
            password:
              password.trim(),
          }
        );

      const token =
        res.data?.token;

      const user =
        res.data?.user;

      if (!token || !user) {
        throw new Error(
          "Invalid login response."
        );
      }

      saveSession(
        token,
        user
      );

      return {
        success: true,
        token,
        user,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          error.message ||
          "Login failed.",
      };
    }
  };

/* =========================================
   REGISTER
========================================= */
export const registerUser =
  async ({
    name,
    email,
    password,
  }) => {
    try {
      const res =
        await api.post(
          "/auth/register",
          {
            name:
              name.trim(),
            email:
              email.trim(),
            password:
              password.trim(),
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
          "Registration failed.",
      };
    }
  };

/* =========================================
   LOGOUT
========================================= */
export const logoutUser =
  () => {
    clearSession();

    return {
      success: true,
    };
  };

/* =========================================
   VERIFY SESSION
========================================= */
export const verifySession =
  async () => {
    try {
      const res =
        await api.get(
          "/auth/me"
        );

      const user =
        res.data?.user ||
        res.data;

      if (user) {
        localStorage.setItem(
          USER_KEY,
          JSON.stringify(
            user
          )
        );
      }

      return {
        success: true,
        user,
      };
    } catch (error) {
      clearSession();

      throw {
        success: false,
        message:
          "Session expired.",
      };
    }
  };

/* =========================================
   UPDATE PROFILE
========================================= */
export const updateProfile =
  async (payload) => {
    try {
      const res =
        await api.put(
          "/auth/profile",
          payload
        );

      const user =
        res.data?.user ||
        res.data;

      localStorage.setItem(
        USER_KEY,
        JSON.stringify(
          user
        )
      );

      return {
        success: true,
        user,
      };
    } catch (error) {
      throw {
        success: false,
        message:
          "Profile update failed.",
      };
    }
  };

/* =========================================
   CHANGE PASSWORD
========================================= */
export const changePassword =
  async ({
    currentPassword,
    newPassword,
  }) => {
    try {
      const res =
        await api.post(
          "/auth/change-password",
          {
            currentPassword,
            newPassword,
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
          "Password change failed.",
      };
    }
  };