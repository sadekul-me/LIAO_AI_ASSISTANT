import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Context Providers
import { ThemeProvider } from './context/ThemeContext'
import { AuthProvider } from './context/AuthContext'
import { AIProvider } from './context/AIContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <AIProvider>
          <App />
        </AIProvider>
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>,
)