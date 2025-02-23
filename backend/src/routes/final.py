import tempfile
import os
import sys
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI


sys.path.append("..")
from controllers import (
    supabase_handler,
    openai_chat_controller,
    tts_controller,
    langchain_rag,
)

client = OpenAI()


class FinalRequest(BaseModel):
    character: str
    text_input: Optional[str] = None
    voice_repo: Optional[str] = (
        "s3://voice-cloning-zero-shot/a9cabd69-695e-48a2-a96d-1f237840c7bc/original/manifest.json"
    )


final_router = APIRouter(prefix="/final")


@final_router.post("/")
async def final_function(request: FinalRequest) -> Dict[str, Any]:
    try:
        if request.text_input:
            transcribed_text = request.text_input
            rag_context = await langchain_rag.vector_retrieval(transcribed_text)
            print("RAG Context:", rag_context)
            characterized_response = openai_chat_controller(
                context={
                    "name": "Daniel",
                    "emotion": "happy",
                    "rag_context": rag_context,
                },
                prompt=transcribed_text,
            )

            print("Characterized Response:", characterized_response)

            if not characterized_response:
                return {"status": 404, "message": "No response generated"}

            tts_class = tts_controller.TTSController()

            print("Voice Repo:", request.voice_repo)

            tts_class.convert_text_to_speech(
                text=characterized_response, voice=request.voice_repo
            )

            print("Characterized Response:", characterized_response)

            return {
                "transcribed_text": transcribed_text,
                "characterized_response": characterized_response,
                "rag_context": rag_context,
            }

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
            # transcribed_text = "Hi TED How are you?"

            print("Transcribed Text:", transcribed_text)

            rag_context = await langchain_rag.vector_retrieval(transcribed_text)

            print("RAG Context:", rag_context)

            characterized_response = openai_chat_controller(
                context={
                    "name": "Daniel",
                    "emotion": "happy",
                    "rag_context": rag_context,
                },
                prompt=transcribed_text,
            )
            # TODO: make emotion and name dynamic

            print("Characterized Response:", characterized_response)

            if not characterized_response:
                return {"status": 404, "message": "No response generated"}

            tts_class = tts_controller.TTSController()

            tts_class.convert_text_to_speech(characterized_response, request.voice_repo)

            return {
                "transcribed_text": transcribed_text,
                "characterized_response": characterized_response,
                "rag_context": rag_context,
            }
        return {"status_code": 404, "detail": "No new audio found"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
