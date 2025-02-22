import os

from fastapi import APIRouter, Depends, HTTPException

import sys
sys.path.append("..")
from controllers import tts_controller

tts_router = APIRouter(prefix="/tts")

# XOXO -> Our PlayHT API key and user ID
tts_controller = tts_controller.TTSController(PLAYHT_API_KEY=os.getenv("PLAYHT_API_KEY"), PLAYHT_USER_ID=os.getenv("PLAYHT_USERID"))

@tts_router.post("/convert")
async def convert_text_to_speech(text: str, voice: str):
    try:
        result = tts_controller.convert_text_to_speech(text, voice)
        return {"status": "success", "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tts_router.get("/speech/{transcription_id}")
async def get_speech(transcription_id: str):
    try:
        result = tts_controller.get_speech(transcription_id)
        return {"status": "success", "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))