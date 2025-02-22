from fastapi import HTTPException, APIRouter
from services.tts_service import generate_speech
from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    voice_id: str

