import { useState, useEffect, useCallback } from "react";

/* ==================================================
   useAuth Hook
   Clean / Local Auth Ready / Scalable
================================================== */

export default function useAuth() {
  const STORAGE_USER = "liao_auth_user";
  const STORAGE_TOKEN = "liao_auth_token";

  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");
  const [isAuthenticated, setIsAuthenticated] =
    useState(false);

  const [isLoading, setIsLoading] =
    useState(true);

  const [error, setError] = useState(null);

  /* =========================================
     INIT
  ========================================= */
  useEffect(() => {
    try {
      const savedUser =
        localStorage.getItem(STORAGE_USER);

      const savedToken =
        localStorage.getItem(STORAGE_TOKEN);

      if (savedUser && savedToken) {
        setUser(JSON.parse(savedUser));
        setToken(savedToken);
        setIsAuthenticated(true);
      }
    } catch (err) {
      console.warn("Auth load error:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /* =========================================
     HELPERS
  ========================================= */
  const persistAuth = useCallback(
    (userData, authToken) => {
      localStorage.setItem(
        STORAGE_USER,
        JSON.stringify(userData)
      );

      localStorage.setItem(
        STORAGE_TOKEN,
        authToken
      );
    },
    []
  );

  const clearStorage = useCallback(() => {
    localStorage.removeItem(STORAGE_USER);
    localStorage.removeItem(STORAGE_TOKEN);
  }, []);

  /* =========================================
     LOGIN
  ========================================= */
  const login = useCallback(
    async ({
      email = "",
      password = "",
      name = "User",
    }) => {
      setIsLoading(true);
      setError(null);

      try {
        const cleanEmail = email.trim();
        const cleanPassword =
          password.trim();

        if (!cleanEmail || !cleanPassword) {
          throw new Error(
            "Email and password required."
          );
        }

        const fakeToken =
          "liao_" +
          Date.now() +
          "_" +
          Math.random()
            .toString(36)
            .slice(2, 8);

        const userData = {
          id: Date.now(),
          name,
          email: cleanEmail,
          role: "user",
        };

        setUser(userData);
        setToken(fakeToken);
        setIsAuthenticated(true);

        persistAuth(userData, fakeToken);

        return {
          success: true,
          user: userData,
        };
      } catch (err) {
        setError(
          err.message ||
            "Login failed."
        );

        return {
          success: false,
        };
      } finally {
        setIsLoading(false);
      }
    },
    [persistAuth]
  );

  /* =========================================
     REGISTER
  ========================================= */
  const register = useCallback(
    async ({
      name = "",
      email = "",
      password = "",
    }) => {
      return await login({
        name,
        email,
        password,
      });
    },
    [login]
  );

  /* =========================================
     LOGOUT
  ========================================= */
  const logout = useCallback(() => {
    setUser(null);
    setToken("");
    setIsAuthenticated(false);
    setError(null);

    clearStorage();
  }, [clearStorage]);

  /* =========================================
     UPDATE PROFILE
  ========================================= */
  const updateProfile = useCallback(
    (data = {}) => {
      if (!user) return;

      const updatedUser = {
        ...user,
        ...data,
      };

      setUser(updatedUser);

      localStorage.setItem(
        STORAGE_USER,
        JSON.stringify(updatedUser)
      );
    },
    [user]
  );

  /* =========================================
     CHECK TOKEN
  ========================================= */
  const validateSession = useCallback(() => {
    return !!token && isAuthenticated;
  }, [token, isAuthenticated]);

  /* =========================================
     EXPORT
  ========================================= */
  return {
    user,
    token,

    isAuthenticated,
    isLoading,
    error,

    login,
    register,
    logout,

    updateProfile,
    validateSession,
  };
}