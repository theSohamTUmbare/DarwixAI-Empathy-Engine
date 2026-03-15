from fastapi import APIRouter, Form
from app.services.empathy_service import generate_emotional_voice

router = APIRouter()


@router.post("/speak")
async def speak(text: str = Form(...)):

    audio = await generate_emotional_voice(text)

    return {
        "audio": audio
    }
