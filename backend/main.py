from fastapi import FastAPI

from backend.api.chat_api import router as chat_router


app = FastAPI(
    title="LIAO AI Assistant",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "running",
        "project": "LIAO AI Assistant"
    }


app.include_router(chat_router)