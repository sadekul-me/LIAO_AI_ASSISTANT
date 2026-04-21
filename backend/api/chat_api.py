from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.core.ai_engine import AIEngine


# ==================================================
# ROUTER
# ==================================================
router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# AI Engine Load
ai_engine = AIEngine()


# ==================================================
# REQUEST / RESPONSE MODELS
# ==================================================
class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    context: str = Field(default="")


class ChatResponse(BaseModel):
    success: bool
    reply: str
    provider: str = "unknown"


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


# ==================================================
# MAIN CHAT ENDPOINT
# ==================================================
@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        user_message = request.message.strip()

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        print("=" * 50)
        print("🟢 USER MESSAGE:", user_message)

        # Generate response
        reply = ai_engine.generate_response(
            user_input=user_message,
            context=request.context
        )

        provider = getattr(
            ai_engine,
            "last_provider",
            "unknown"
        )

        if not reply:
            reply = "আমি এখন উত্তর দিতে পারছি না।"

        print("🤖 AI REPLY:", reply)
        print("⚙️ PROVIDER:", provider)
        print("=" * 50)

        return ChatResponse(
            success=True,
            reply=reply,
            provider=provider
        )

    except HTTPException as e:
        print("⚠️ HTTP ERROR:", e.detail)
        raise e

    except Exception as e:
        print("🔥 CHAT API CRASH:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Server Error: {str(e)}"
        )


# ==================================================
# INTENT DETECTION
# ==================================================
@router.post("/intent")
def detect_intent(request: ChatRequest):
    try:
        text = request.message.strip()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        print("=" * 50)
        print("🧠 INTENT INPUT:", text)

        result = ai_engine.detect_intent(text)

        if not result:
            result = {
                "intent": "chat",
                "target": "",
                "message": ""
            }

        print("🧠 INTENT OUTPUT:", result)
        print("=" * 50)

        return {
            "success": True,
            "data": result
        }

    except HTTPException as e:
        print("⚠️ INTENT HTTP ERROR:", e.detail)
        raise e

    except Exception as e:
        print("🔥 INTENT ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Intent Error: {str(e)}"
        )


# ==================================================
# TEST ENDPOINT
# ==================================================
@router.get("/ping")
def ping():
    return {
        "success": True,
        "message": "Chat API running perfectly."
    }