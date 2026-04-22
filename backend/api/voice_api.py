from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

import tempfile

from backend.services.speech_to_text import SpeechToTextService
from backend.services.text_to_speech import TextToSpeechService


# ==================================================
# ROUTER
# ==================================================
router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)

# Services
stt = SpeechToTextService()
tts = TextToSpeechService()


# ==================================================
# REQUEST MODEL
# ==================================================
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


# ==================================================
# 🧰 HELPERS
# ==================================================
def _save_temp_file(audio_bytes: bytes) -> str:
    """
    Save uploaded audio to temporary wav file
    """
    try:
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        temp_file.write(audio_bytes)
        temp_file.close()

        return temp_file.name

    except Exception as e:
        print("TEMP FILE ERROR:", str(e))
        return ""


# ==================================================
# 🎤 SPEECH TO TEXT
# ==================================================
@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(
                status_code=400,
                detail="Audio file is required"
            )

        audio_bytes = await file.read()

        if not audio_bytes:
            return JSONResponse({
                "success": False,
                "text": "",
                "error": "Empty audio file"
            })

        file_path = _save_temp_file(audio_bytes)

        if not file_path:
            return JSONResponse({
                "success": False,
                "text": "",
                "error": "Failed to save audio file"
            })

        # FIXED: correct service method
        result = stt.transcribe_wav_file(file_path=file_path)

        return JSONResponse({
            "success": result.get("success", False),
            "text": result.get("text", ""),
            "error": result.get("message", None)
        })

    except Exception as e:
        print("STT ERROR:", str(e))

        return JSONResponse({
            "success": False,
            "text": "",
            "error": str(e)
        })


# ==================================================
# 🔊 TEXT TO SPEECH
# ==================================================
@router.post("/tts")
async def text_to_speech(payload: TTSRequest):
    try:
        text = payload.text.strip()

        if not text:
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )

        # FIXED: correct service call
        result = tts.speak(text)

        if not result or not result.get("success"):
            return JSONResponse({
                "success": False,
                "audio_path": None,
                "error": "TTS generation failed"
            })

        return JSONResponse({
            "success": True,
            "audio_path": result.get("audio_path", None),
            "error": None
        })

    except HTTPException as e:
        raise e

    except Exception as e:
        print("TTS ERROR:", str(e))

        return JSONResponse({
            "success": False,
            "audio_path": None,
            "error": str(e)
        })