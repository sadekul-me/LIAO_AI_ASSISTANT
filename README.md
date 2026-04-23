# LIAO AI Assistant

LIAO AI Assistant is a full-stack local AI assistant system designed to interact with the computer using text, voice, and automation. It provides intelligent conversation, system control, and productivity features through a modular and scalable architecture.

The system is designed to run locally for privacy, speed, and full user control.

---

# Project Overview

LIAO AI Assistant works as a bridge between human intent and system execution. It processes natural language input and performs actions through structured backend services and a modern React.js frontend interface.

---

# System Architecture

The project is divided into two main parts:

- 🧠 Backend (Python / FastAPI) → AI engine, automation, system control  
- 💻 Frontend (React.js) → UI, chat interface, voice interaction, dashboard  

---

# Features

## AI System
- Natural language chat system  
- Context-aware responses  
- Personality-driven interaction  
- Memory-based conversation handling  

## Voice System
- Speech-to-text input  
- Text-to-speech output  
- Wake word detection support  

## System Control
- Application automation  
- File and folder management  
- System-level commands  

## Browser Automation
- Web search handling  
- Navigation automation  
- Task-based browsing  

## Frontend UI
- Real-time chat interface  
- Voice interaction UI  
- AI avatar visualization  
- Settings panel  
- Responsive dashboard  

---

# Backend Structure

```bash
backend/
│
├── api/
├── core/
├── services/
├── automation/
├── security/
├── database/
├── utils/
├── voice_engine/
├── integrations/
├── data/
├── tests/
├── scripts/
├── config/
├── main.py
```

```
Frontend Structure (React.js)
src/
│
├── components/
│   ├── layout/
│   │   ├── Sidebar.jsx
│   │   ├── Topbar.jsx
│   │   └── MainLayout.jsx
│   │
│   ├── chat/
│   │   ├── ChatPanel.jsx
│   │   ├── ChatMessage.jsx
│   │   └── ChatInput.jsx
│   │
│   ├── ai/
│   │   ├── Avatar.jsx
│   │   └── VoiceWave.jsx
│   │
│   └── settings/
│       └── SettingsPanel.jsx
│
├── pages/
│   └── Dashboard.jsx
│
├── hooks/
│   └── useAI.js
│
├── services/
│   └── api.js
│
├── styles/
│   └── global.css
│
├── App.jsx
└── main.jsx
```
Technology Stack
Backend
Python
FastAPI
SQLite
SQLAlchemy
Whisper / Speech Recognition
Edge TTS
PyAutoGUI
Frontend
React.js
JavaScript (ES6+)
CSS
Fetch / Axios API handling
Setup
Backend
git clone <repo-url>
cd LIAO_AI_ASSISTANT
pip install -r requirements.txt
uvicorn backend.main:app --reload
Frontend
cd frontend
npm install
npm run dev
Environment Variables
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
OPENROUTER_API_KEY=your_key
License

LIAO AI Assistant Source License v1.0

Copyright (c) 2026 Sadekul Islam
All rights reserved.

This software is proprietary. Unauthorized use, copying, modification, or distribution is strictly prohibited.