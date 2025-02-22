from fastapi import APIRouter, HTTPException

import sys
sys.path.append("..")
from controllers import aws_transcribe

sst_router = APIRouter(prefix="/sst")

@sst_router.post("/")
async def transcribe(job_name: str, job_uri: str, media_format: str = 'mp3', language_code: str = 'en-US'):
    try:
        transcript_data = aws_transcribe.transcribe_audio(job_name, job_uri, media_format, language_code)
        return {"transcript": transcript_data['results']['transcripts'][0]['transcript']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))