import tempfile
import os
import sys
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI


sys.path.append("..")
from controllers import supabase_handler, openai_chat_controller, tts_controller

client = OpenAI()


class TranscribeRequest(BaseModel):
    job_name: str
    job_uri: str
    media_format: str = "mp3"
    language_code: str = "en-US"


final_router = APIRouter(prefix="/final")


@final_router.post("/")
async def final_function(character: str, voice_repo: str='') -> Dict[str, Any]:
    try:
        latest_audio = await supabase_handler.fetch_latest_user_audio_from_supabase()
        if latest_audio:

            # Create a temporary file with .mp3 extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(latest_audio)
                temp_file_path = temp_file.name

            # Use OpenAI's API to transcribe
            with open(temp_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, language="en"
                )

            # Clean up the temporary file
            os.unlink(temp_file_path)
            transcribed_text = transcription.text
            
            characterized_response = openai_chat_controller(character=character, prompt=transcribed_text)
            
            if not characterized_response:
                return {"status": 404, "message": "No response generated"}
            
            tts_controller.convert_text_to_speech(characterized_response.script, characterized_response.voice)
            
            return {
                "status": 200,
                "transcribed_text": transcribed_text,
                "characterized_response": characterized_response.script,
                "voice": characterized_response.voice
            }
        return {"status": 404, "message": "No new audio found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
