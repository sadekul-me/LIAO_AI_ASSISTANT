// context/AuthContext.jsx

import { createContext, useState, useEffect } from "react";
import api from "../services/api";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);

  // 🔹 Load user on app start
  useEffect(() => {
    const loadUser = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const res = await api.get("/auth/me");
        setUser(res.data);
      } catch (err) {
        console.error("Auth load error:", err);
        logout();
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [token]);

  // 🔹 Login
  const login = async (credentials) => {
    try {
      const res = await api.post("/auth/login", credentials);
      const { token: newToken, user } = res.data;

      setToken(newToken);
      setUser(user);
      localStorage.setItem("token", newToken);
    } catch (err) {
      console.error("Login error:", err);
      throw err;
    }
  };

  // 🔹 Logout
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};