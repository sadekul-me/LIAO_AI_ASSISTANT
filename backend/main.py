from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat_api import router as chat_router
from backend.api.voice_api import router as voice_router


# ==================================================
# APP INIT
# ==================================================
app = FastAPI(
    title="LIAO AI Assistant",
    version="1.0.0",
    description="Local AI Assistant Backend System (Jarvis Core)"
)


# ==================================================
# CORS CONFIG
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production এ restrict করা লাগবে
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# ROOT ENDPOINT
# ==================================================
@app.get("/")
def home():
    return {
        "status": "running",
        "project": "LIAO AI Assistant",
        "mode": "Jarvis AI System"
    }


# ==================================================
# HEALTH CHECK
# ==================================================
@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "System is healthy",
        "status": "ok"
    }


# ==================================================
# SYSTEM STATUS
# ==================================================
@app.get("/system/status")
def system_status():
    return {
        "status": "online",
        "project": "LIAO AI Assistant",
        "engine": "Jarvis Core Active",
        "version": "1.0.0"
    }


# ==================================================
# ROUTES
# ==================================================
app.include_router(chat_router)
app.include_router(voice_router)


# ==================================================
# STARTUP EVENT
# ==================================================
@app.on_event("startup")
def startup_event():
    print("\n" + "=" * 55)
    print("🚀 LIAO AI Assistant Backend Started")
    print("🧠 Jarvis Core: ACTIVE")
    print("📡 Server: http://127.0.0.1:8000")
    print("📘 Docs: http://127.0.0.1:8000/docs")
    print("=" * 55 + "\n")


# ==================================================
# MAIN RUN
# ==================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )