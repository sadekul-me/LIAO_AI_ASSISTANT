# LIAO AI Assistant

LIAO AI Assistant is a desktop-based intelligent assistant system designed to help users interact with their computer using natural language, voice commands, and automation tools.

The project focuses on building a modular, extensible, and secure assistant capable of handling everyday computer tasks such as application control, file management, browsing, and system operations.

---

## 📌 Project Overview

This system acts as a local assistant that runs on a user's machine and provides an interactive interface for executing commands through text or voice input.

The assistant is structured to separate core logic, services, APIs, and automation layers for better maintainability and scalability.

---

## 🎯 Key Features

- Voice-based interaction system
- Text-based chat interface
- Application and system control
- Browser automation
- File and directory management
- Modular API architecture
- Local database for memory storage
- Extensible service-based design

---

## 🧱 Project Architecture

The project follows a modular structure:

- **backend/** → Core logic, APIs, services, and automation
- **voice_engine/** → Voice processing and wake word detection
- **config/** → Configuration and system settings
- **data/** → Local storage and logs
- **integrations/** → External service integrations
- **frontend/** → Optional user interface
- **tests/** → Unit testing modules
- **scripts/** → Setup and automation scripts

---

## ⚙️ Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Text-to-Speech (Edge TTS)
- Speech Recognition (Whisper or equivalent)
- Automation tools (PyAutoGUI)
- REST API architecture

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repo-url>
cd LIAO_AI_ASSISTANT