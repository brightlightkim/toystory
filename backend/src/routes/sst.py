import tempfile
import os
import sys
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI


sys.path.append("..")
from controllers import aws_transcribe, supabase_handler

client = OpenAI()


class TranscribeRequest(BaseModel):
    job_name: str
    job_uri: str
    media_format: str = "mp3"
    language_code: str = "en-US"


sst_router = APIRouter(prefix="/sst")


@sst_router.get("/")
async def get_recent_sst() -> Dict[str, Any]:
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
            return {
                "status": 200,
                "transcribed_text": transcribed_text,
            }
        return {"status": 404, "message": "No new audio found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sst_router.post("/transcribe")
async def transcribe(request: TranscribeRequest) -> Dict[str, Any]:
    try:
        transcript_data = await aws_transcribe.transcribe_audio(
            request.job_name,
            request.job_uri,
            request.media_format,
            request.language_code,
        )
        return {
            "status": 200,
            "transcript": transcript_data["results"]["transcripts"][0]["transcript"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
