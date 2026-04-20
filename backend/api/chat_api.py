from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.ai_engine import AIEngine


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

ai_engine = AIEngine()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    context: str = Field(default="")


class ChatResponse(BaseModel):
    success: bool
    reply: str


@router.get("/")
def chat_status():
    """
    Health check for chat service.
    """
    return {
        "service": "chat",
        "status": "online"
    }


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Receives user message and returns assistant response.
    """
    try:
        user_message = request.message.strip()

        if not user_message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        reply = ai_engine.generate_response(
            user_input=user_message,
            context=request.context
        )

        return ChatResponse(
            success=True,
            reply=reply
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process request at this time."
        )


@router.post("/intent")
def detect_intent(request: ChatRequest):
    """
    Detect user intent for command routing.
    """
    try:
        result = ai_engine.detect_intent(request.message)

        return {
            "success": True,
            "data": result
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Intent detection failed."
        )