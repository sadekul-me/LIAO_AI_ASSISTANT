from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from backend.services.speech_to_text import SpeechToText
from backend.services.text_to_speech import TextToSpeech


router = APIRouter()

stt = SpeechToText()
tts = TextToSpeech()


# -----------------------------
# 🎤 Speech to Text API
# -----------------------------
@router.post("/voice/stt")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Convert voice audio to text
    """

    try:
        audio_bytes = await file.read()

        text = stt.convert(audio_bytes)

        return JSONResponse({
            "success": True,
            "text": text
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


# -----------------------------
# 🔊 Text to Speech API
# -----------------------------
@router.post("/voice/tts")
async def text_to_speech(payload: dict):
    """
    Convert text to speech audio
    """

    try:
        text = payload.get("text", "")

        if not text:
            return JSONResponse({
                "success": False,
                "error": "No text provided"
            })

        audio_path = tts.speak(text)

        return JSONResponse({
            "success": True,
            "audio_path": audio_path
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })