from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import time
import traceback

from backend.core.ai_engine import AIEngine

# ==================================================
# 🚀 LIAO CHAT API ULTRA PRO v3
# Fast / Clean / Production Ready
# ==================================================

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# ==================================================
# GLOBAL AI ENGINE (Single Instance = Faster)
# ==================================================
ai_engine = AIEngine()

# ==================================================
# SIMPLE MEMORY CACHE
# ==================================================
server_started = datetime.now()
total_requests = 0
total_errors = 0


# ==================================================
# SCHEMAS
# ==================================================
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: str = Field(default="default_user")


class ChatResponse(BaseModel):
    success: bool
    reply: str
    provider: str
    latency: float
    timestamp: str


# ==================================================
# UTILITIES
# ==================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text: str) -> str:
    return text.strip().replace("\n", " ").replace("\r", "")


# ==================================================
# STATUS
# ==================================================
@router.get("")
def chat_status():
    return {
        "service": "chat",
        "status": "online",
        "ai_ready": True,
        "provider": getattr(ai_engine, "last_provider", "offline"),
        "uptime": str(datetime.now() - server_started).split(".")[0],
        "requests": total_requests,
        "errors": total_errors,
        "time": now()
    }


@router.get("/ping")
def ping():
    return {
        "success": True,
        "message": "LIAO Chat API Online",
        "time": now()
    }


@router.get("/stats")
def stats():
    return {
        "uptime": str(datetime.now() - server_started).split(".")[0],
        "requests": total_requests,
        "errors": total_errors,
        "provider": getattr(ai_engine, "last_provider", "offline"),
        "latency": getattr(ai_engine, "last_latency", 0)
    }


# ==================================================
# MAIN CHAT API
# ==================================================
@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    global total_requests, total_errors
    total_requests += 1

    start = time.time()

    try:
        user_message = clean_text(request.message)

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        print("\n" + "=" * 60)
        print(f"USER ({request.session_id}): {user_message}")

        # Generate AI Reply
        reply = ai_engine.generate_response(
            user_input=user_message,
            session_id=request.session_id
        )

        provider = getattr(ai_engine, "last_provider", "offline")

        if not reply:
            reply = "I am unable to respond right now."

        latency = round(time.time() - start, 3)

        print(f"REPLY: {reply}")
        print(f"PROVIDER: {provider}")
        print(f"LATENCY: {latency}s")
        print("=" * 60 + "\n")

        return ChatResponse(
            success=True,
            reply=reply,
            provider=provider,
            latency=latency,
            timestamp=now()
        )

    except HTTPException as e:
        total_errors += 1
        raise e

    except Exception as e:
        total_errors += 1

        print("SYSTEM ERROR:", str(e))
        traceback.print_exc()

        return ChatResponse(
            success=False,
            reply="Internal server error.",
            provider="error",
            latency=0,
            timestamp=now()
        )


# ==================================================
# INTENT DETECTION
# ==================================================
@router.post("/intent")
def detect_intent(request: ChatRequest):

    try:
        text = clean_text(request.message)

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Empty message"
            )

        if hasattr(ai_engine, "detect_intent"):
            result = ai_engine.detect_intent(text)
        else:
            result = {
                "intent": "chat",
                "target": "",
                "action": ""
            }

        return {
            "success": True,
            "data": result,
            "time": now()
        }

    except Exception as e:
        return {
            "success": False,
            "data": {
                "intent": "chat",
                "target": "",
                "action": ""
            },
            "error": str(e)
        }


# ==================================================
# QUICK TEST
# ==================================================
@router.get("/test/{msg}")
def quick_test(msg: str):

    try:
        reply = ai_engine.generate_response(msg)

        return {
            "success": True,
            "message": msg,
            "reply": reply,
            "provider": getattr(ai_engine, "last_provider", "offline")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================================================
# RESET STATS
# ==================================================
@router.post("/reset")
def reset_stats():

    global total_requests, total_errors

    total_requests = 0
    total_errors = 0

    return {
        "success": True,
        "message": "Stats reset complete."
    }