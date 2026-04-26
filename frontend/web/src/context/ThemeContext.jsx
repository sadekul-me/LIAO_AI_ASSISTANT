import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('dark'); // ডিফল্ট ডার্ক থিম
  const [accentColor, setAccentColor] = useState('#3B82F6'); // ছবির সেই নীল কালার

  // থিম পরিবর্তনের সাথে সাথে ডোমেইন লেভেলে ক্লাস অ্যাড করা
  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    
    // লোকাল স্টোরেজে সেভ করে রাখা
    localStorage.setItem('liao-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <ThemeContext.Provider value={{ 
      theme, 
      toggleTheme, 
      accentColor, 
      setAccentColor 
    }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};