import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# ================================
# 🔥 ROUTERS (IMPORTANT)
# ================================
from backend.api.chat_api import router as chat_router
from backend.api.voice_api import router as voice_router
from backend.api.command_api import router as command_router  # ✅ FIXED

# ================================
# 🔥 APP LIFECYCLE (BETTER THAN on_event)
# ================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "=" * 55)
    print("🚀 LIAO AI Assistant Backend Started")
    print("🧠 Jarvis Core: ACTIVE")
    print("📡 Server: http://127.0.0.1:8000")
    print("📘 Docs: http://127.0.0.1:8000/docs")
    print("📂 Static Path: http://127.0.0.1:8000/static")
    print("=" * 55 + "\n")

    yield

    print("\n🛑 Server shutting down...\n")


# ================================
# 🚀 APP INIT
# ================================
app = FastAPI(
    title="LIAO AI Assistant",
    version="2.0.0",
    description="🔥 Ultra Jarvis AI System",
    lifespan=lifespan
)

# ================================
# 📂 STATIC FILES
# ================================
STATIC_DIR = "static"

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ================================
# 🌐 CORS
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🔒 production এ restrict করবি
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# 🏠 ROOT
# ================================
@app.get("/")
def home():
    return {
        "status": "running",
        "project": "LIAO AI Assistant",
        "mode": "ULTRA JARVIS",
        "version": "2.0.0"
    }

# ================================
# ❤️ HEALTH
# ================================
@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "System is healthy",
        "status": "ok"
    }

# ================================
# ⚙️ SYSTEM STATUS
# ================================
@app.get("/system/status")
def system_status():
    return {
        "status": "online",
        "engine": "Jarvis Core Active",
        "modules": [
            "chat",
            "voice",
            "command",
            "automation"
        ]
    }

# ================================
# 🔥 ROUTES (MOST IMPORTANT)
# ================================
app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(command_router)  # 💥 THIS FIXES YOUR ERROR

# ================================
# 🧪 DEBUG ROUTE (VERY USEFUL)
# ================================
@app.get("/debug/routes")
def list_routes():
    return [route.path for route in app.routes]

# ================================
# 🚀 MAIN RUN
# ================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )