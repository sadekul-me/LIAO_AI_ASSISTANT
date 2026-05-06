import os
import uuid
import time
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

# ==================================================
# SERVICES
# ==================================================
from backend.services.speech_to_text import SpeechToTextService
from backend.services.text_to_speech import TextToSpeechService
from backend.core.ai_engine import AIEngine

# ==================================================
# ROUTER INIT
# ==================================================
router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)

# ==================================================
# SINGLETON SERVICES (OPTIMIZED)
# ==================================================
stt = SpeechToTextService()
tts = TextToSpeechService()
ai = AIEngine()

# ==================================================
# PATH CONFIG
# ==================================================
BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

# ==================================================
# CONFIG
# ==================================================
MAX_AUDIO_SIZE_MB = 10
AUDIO_EXPIRY_SEC = 3600

# ==================================================
# REQUEST MODELS
# ==================================================
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class AskRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=3000)
    session_id: str = Field(default="voice_user")


# ==================================================
# RESPONSE HELPERS
# ==================================================
def success(data: Dict[str, Any]):
    return JSONResponse({"success": True, **data})


def fail(message: str):
    return JSONResponse({"success": False, "error": message})


# ==================================================
# FILE HELPERS
# ==================================================
def remove_file_safe(path: Path):
    try:
        if path.exists():
            path.unlink()
    except:
        pass


def clean_old_audio_files():
    try:
        now = time.time()

        for file in STATIC_DIR.glob("liao_voice_*.mp3"):
            if now - file.stat().st_mtime > AUDIO_EXPIRY_SEC:
                remove_file_safe(file)

    except:
        pass


def validate_audio(file: UploadFile):
    if not file:
        raise HTTPException(400, "Audio file required")

    if file.size and file.size > MAX_AUDIO_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, "Audio too large")


# ==================================================
# 🧠 SMART COMMAND DETECTION (VOICE)
# ==================================================
def is_voice_command(text: str) -> bool:
    triggers = [
        "open", "run", "create", "write", "search",
        "shutdown", "restart",
        "খুলো", "চালাও", "তৈরি", "লিখ", "খুঁজ"
    ]
    return any(t in text.lower() for t in triggers)


# ==================================================
# 🎤 SPEECH TO TEXT
# ==================================================
@router.post("/stt")
async def speech_to_text(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    try:
        validate_audio(file)

        ext = file.filename.split(".")[-1] if file.filename else "wav"

        temp_path = STATIC_DIR / f"upload_{uuid.uuid4().hex}.{ext}"

        audio_bytes = await file.read()

        if not audio_bytes:
            return fail("Empty audio")

        with open(temp_path, "wb") as f:
            f.write(audio_bytes)

        result = stt.transcribe_wav_file(str(temp_path))

        background_tasks.add_task(remove_file_safe, temp_path)

        return success({
            "text": result.get("text", ""),
            "message": result.get("message", "")
        })

    except Exception as e:
        return fail(str(e))


# ==================================================
# 🔊 TEXT TO SPEECH
# ==================================================
@router.post("/tts")
async def text_to_speech(
    payload: TTSRequest,
    background_tasks: BackgroundTasks
):
    try:
        text = payload.text.strip()

        if not text:
            return fail("Text empty")

        clean_old_audio_files()

        file_name = f"liao_voice_{uuid.uuid4().hex[:8]}.mp3"
        output_path = STATIC_DIR / file_name

        result = tts.speak(text=text, output_path=str(output_path))

        if not result.get("success"):
            return fail(result.get("error", "TTS failed"))

        return success({
            "audio_path": file_name
        })

    except Exception as e:
        return fail(str(e))


# ==================================================
# 🤖 FULL VOICE PIPELINE (🔥 JARVIS MODE)
# STT → INTENT → ACTION/AI → TTS
# ==================================================
@router.post("/ask")
async def ask_voice(
    payload: AskRequest,
    background_tasks: BackgroundTasks
):
    try:
        text = payload.text.strip()

        if not text:
            return fail("Text empty")

        start = time.time()

        # ==================================================
        # 🧠 AI INTENT DETECTION
        # ==================================================
        decision = ai.detect_intent(text)

        # ==================================================
        # ⚙️ COMMAND MODE (VOICE → ACTION)
        # ==================================================
        if decision.get("intent") != "chat":

            reply = ai._handle_action(decision)

        else:
            # ==================================================
            # 💬 NORMAL AI CHAT
            # ==================================================
            reply = ai.generate_response(
                user_input=text,
                session_id=payload.session_id
            )

        provider = ai.last_provider

        # ==================================================
        # 🔊 TTS GENERATION
        # ==================================================
        clean_old_audio_files()

        file_name = f"liao_voice_{uuid.uuid4().hex[:8]}.mp3"
        output_path = STATIC_DIR / file_name

        tts_result = tts.speak(
            text=reply,
            output_path=str(output_path)
        )

        audio_file = file_name if tts_result.get("success") else None

        latency = round(time.time() - start, 3)

        return success({
            "user_text": text,
            "reply": reply,
            "provider": provider,
            "latency": latency,
            "audio_path": audio_file
        })

    except Exception as e:
        return fail(str(e))


# ==================================================
# 📊 STATUS
# ==================================================
@router.get("/status")
def get_voice_status():
    return {
        "status": "online",
        "voice_pipeline": "active",
        "stt": "ready",
        "tts": "ready",
        "ai": "connected",
        "static_dir": str(STATIC_DIR)
    }