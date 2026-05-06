from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
import time
import traceback
import requests

from backend.core.ai_engine import AIEngine
from backend.core.decision_engine import DecisionEngine

# ==================================================
# 🚀 LIAO CHAT API ULTRA PRO v5 (REAL JARVIS ROUTER)
# ==================================================

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

ai_engine = AIEngine()
decision_engine = DecisionEngine()

COMMAND_API = "http://127.0.0.1:8000/command/execute"

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
# UTIL
# ==================================================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean(text: str):
    return text.strip()


# ==================================================
# 🔥 SMART COMMAND DETECTION (AI BASED)
# ==================================================
def should_execute(decision: Dict[str, Any]) -> bool:
    """
    👉 Only execute if it's real action intent
    """
    return decision.get("intent") not in ["chat", "empty"]


# ==================================================
# MAIN CHAT
# ==================================================
@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    global total_requests, total_errors
    total_requests += 1

    start = time.time()

    try:
        user_message = clean(request.message)

        print("\n" + "=" * 60)
        print(f"USER: {user_message}")

        # ==================================================
        # 🧠 DECISION ENGINE FIRST (IMPORTANT CHANGE)
        # ==================================================
        decision = decision_engine.analyze(user_message)

        print("🧠 DECISION:", decision)

        # ==================================================
        # ⚙️ COMMAND MODE (SMART)
        # ==================================================
        if should_execute(decision):

            try:
                res = requests.post(
                    COMMAND_API,
                    json={"text": user_message},
                    timeout=5
                )

                if res.status_code == 200:
                    data = res.json()

                    reply = data.get("message", "Done")

                    print("⚙️ COMMAND OK:", data)

                    return ChatResponse(
                        success=True,
                        reply=f"⚡ {reply}",
                        provider="command-engine",
                        latency=round(time.time() - start, 3),
                        timestamp=now()
                    )

                else:
                    print("⚠️ COMMAND API FAILED:", res.text)

            except Exception as e:
                print("❌ COMMAND ERROR:", str(e))

        # ==================================================
        # 🧠 AI CHAT FALLBACK
        # ==================================================
        reply = ai_engine.generate_response(
            user_input=user_message,
            session_id=request.session_id
        )

        provider = getattr(ai_engine, "last_provider", "ai")
        latency = round(time.time() - start, 3)

        print(f"REPLY: {reply}")
        print(f"PROVIDER: {provider}")
        print("=" * 60 + "\n")

        return ChatResponse(
            success=True,
            reply=reply,
            provider=provider,
            latency=latency,
            timestamp=now()
        )

    except Exception as e:
        total_errors += 1

        print("💥 SYSTEM ERROR:", str(e))
        traceback.print_exc()

        return ChatResponse(
            success=False,
            reply="System error occurred.",
            provider="error",
            latency=0,
            timestamp=now()
        )


# ==================================================
# STATUS
# ==================================================
@router.get("/stats")
def stats():
    return {
        "uptime": str(datetime.now() - server_started).split(".")[0],
        "requests": total_requests,
        "errors": total_errors,
        "time": now()
    }


@router.get("/ping")
def ping():
    return {
        "success": True,
        "message": "Jarvis Chat Online 🚀",
        "time": now()
    }