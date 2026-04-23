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
    description="Local AI Assistant Backend System"
)


# ==================================================
# CORS CONFIG (Frontend connect safe)
# ==================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "System is healthy"
    }


# ==================================================
# SYSTEM STATUS ENDPOINT (FIXED)
# ==================================================
@app.get("/system/status")
def system_status():
    return {
        "status": "online",
        "project": "LIAO AI Assistant",
        "version": "1.0.0",
        "message": "System running successfully"
    }


# ==================================================
# ROUTER REGISTRATION
# ==================================================
app.include_router(chat_router)
app.include_router(voice_router)


# ==================================================
# STARTUP EVENT
# ==================================================
@app.on_event("startup")
def startup_event():
    print("\n" + "=" * 50)
    print("🚀 LIAO AI Assistant Backend Started")
    print("📡 Server: http://127.0.0.1:8000")
    print("📘 Docs: http://127.0.0.1:8000/docs")
    print("=" * 50 + "\n")


# ==================================================
# MAIN ENTRY (optional direct run)
# ==================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )