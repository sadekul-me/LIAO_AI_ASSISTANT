import os
import uuid
import time
from pathlib import Path
from typing import Optional

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
# SINGLETON SERVICES
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
# REQUEST MODELS
# ==================================================
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class AskRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=3000)
    session_id: str = Field(default="voice_user")


# ==================================================
# HELPERS
# ==================================================
def success(data: dict):
    return JSONResponse({"success": True, **data})


def fail(message: str):
    return JSONResponse({"success": False, "error": message})


def remove_file_safe(path: Path):
    try:
        if path.exists():
            path.unlink()
    except:
        pass


def clean_old_audio_files():
    """
    Remove generated mp3 older than 1 hour
    """
    try:
        now = time.time()

        for file in STATIC_DIR.glob("liao_voice_*.mp3"):
            age = now - file.stat().st_mtime

            if age > 3600:
                remove_file_safe(file)

    except:
        pass


# ==================================================
# 🎤 SPEECH TO TEXT
# ==================================================
@router.post("/stt")
async def speech_to_text(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Audio file required")

        ext = "wav"

        if file.filename and "." in file.filename:
            ext = file.filename.split(".")[-1].lower()

        temp_name = f"upload_{uuid.uuid4().hex}.{ext}"
        temp_path = STATIC_DIR / temp_name

        audio_bytes = await file.read()

        if not audio_bytes:
            return fail("Empty audio file")

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

        result = tts.speak(
            text=text,
            output_path=str(output_path)
        )

        if not result or not result.get("success"):
            return fail(result.get("error", "TTS failed"))

        return success({
            "audio_path": file_name
        })

    except Exception as e:
        return fail(str(e))


# ==================================================
# 🤖 FULL VOICE AI PIPELINE
# Text -> AI -> TTS
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

        # AI Reply
        reply = ai.generate_response(
            user_input=text,
            session_id=payload.session_id
        )

        provider = ai.last_provider

        # Generate Voice
        clean_old_audio_files()

        file_name = f"liao_voice_{uuid.uuid4().hex[:8]}.mp3"
        output_path = STATIC_DIR / file_name

        tts_result = tts.speak(
            text=reply,
            output_path=str(output_path)
        )

        audio_file = None

        if tts_result and tts_result.get("success"):
            audio_file = file_name

        return success({
            "user_text": text,
            "reply": reply,
            "provider": provider,
            "audio_path": audio_file
        })

    except Exception as e:
        return fail(str(e))


# ==================================================
# STATUS
# ==================================================
@router.get("/status")
def get_voice_status():
    return {
        "status": "online",
        "voice_api": "active",
        "stt_service": "active",
        "tts_service": "active",
        "ai_engine": "active",
        "static_dir": str(STATIC_DIR)
    }