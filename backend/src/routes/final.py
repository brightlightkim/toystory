import tempfile
import os
import sys
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI


sys.path.append("..")
from controllers import supabase_handler, openai_chat_controller, tts_controller

client = OpenAI()


class FinalRequest(BaseModel):
    character: str
    voice_repo: Optional[str] = (
        "s3://voice-cloning-zero-shot/a9cabd69-695e-48a2-a96d-1f237840c7bc/original/manifest.json"
    )


final_router = APIRouter(prefix="/final")


@final_router.post("/")
async def final_function(request: FinalRequest) -> Dict[str, Any]:
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

            print("Transcribed Text:", transcribed_text)

            characterized_response = openai_chat_controller(
                character=request.character, prompt=transcribed_text
            )

            print("Characterized Response:", characterized_response)

            if not characterized_response:
                return {"status": 404, "message": "No response generated"}

            tts_class = tts_controller.TTSController()

            tts_class.convert_text_to_speech(
                characterized_response["script"], request.voice_repo
            )

            return {
                "status": 200,
                "transcribed_text": transcribed_text,
                "characterized_response": characterized_response["script"],
                "voice": characterized_response["voice"],
            }
        return {"status": 404, "message": "No new audio found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
