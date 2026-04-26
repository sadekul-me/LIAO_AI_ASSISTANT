from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.ai_engine import AIEngine

# ==================================================
# ROUTER INIT
# ==================================================
router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

ai_engine = AIEngine()


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


# ==================================================
# HEALTH CHECK
# ==================================================
@router.get("/")
def chat_status():
    return {
        "service": "chat",
        "status": "online",
        "ai_ready": True
    }


@router.get("/ping")
def ping():
    return {
        "success": True,
        "message": "Chat API running properly"
    }


# ==================================================
# MAIN CHAT ENDPOINT (FIXED)
# ==================================================
@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        user_message = request.message.strip()

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="Empty message is not allowed"
            )

        print("\n" + "=" * 50)
        print("USER:", user_message)

        # 🔥 FIX: ONLY session_id pass করো (context না)
        reply = ai_engine.generate_response(
            user_input=user_message,
            session_id=request.session_id
        )

        provider = getattr(ai_engine, "last_provider", "offline")

        if not reply:
            reply = "আমি এখন এই প্রশ্নের উত্তর দিতে পারছি না।"

        print("REPLY:", reply)
        print("PROVIDER:", provider)
        print("=" * 50 + "\n")

        return ChatResponse(
            success=True,
            reply=reply,
            provider=provider
        )

    except HTTPException as e:
        print("HTTP ERROR:", e.detail)
        raise e

    except Exception as e:
        print("SYSTEM ERROR:", str(e))

        return ChatResponse(
            success=False,
            reply="Server error হয়েছে, পরে চেষ্টা করুন।",
            provider="error"
        )


# ==================================================
# INTENT DETECTION (FIXED SAFE VERSION)
# ==================================================
@router.post("/intent")
def detect_intent(request: ChatRequest):
    try:
        text = request.message.strip()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Empty message"
            )

        print("\n" + "=" * 50)
        print("INTENT INPUT:", text)

        # 🔥 SAFE fallback (AIEngine এ detect_intent না থাকলে crash হবে না)
        if hasattr(ai_engine, "detect_intent"):
            result = ai_engine.detect_intent(text)
        else:
            result = {
                "intent": "chat",
                "target": "",
                "action": "",
                "message": "intent engine not found"
            }

        print("INTENT OUTPUT:", result)
        print("=" * 50 + "\n")

        return {
            "success": True,
            "data": result
        }

    except HTTPException as e:
        print("INTENT HTTP ERROR:", e.detail)
        raise e

    except Exception as e:
        print("INTENT ERROR:", str(e))

        return {
            "success": False,
            "data": {
                "intent": "chat",
                "message": "Intent error"
            }
        }