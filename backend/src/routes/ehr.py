import sys
from typing import Dict, Any, Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

sys.path.append("..")
from controllers import openai_ehr_controller, tts_controller, openai_checklist_controller, openai_detection_controller

class EHRRequest(BaseModel):
    query: str
    character: str
    voice_repo: Optional[str] = (
        "s3://voice-cloning-zero-shot/a9cabd69-695e-48a2-a96d-1f237840c7bc/original/manifest.json"
    )

class EHRCheckRequest(BaseModel):
    checklist: dict
    conversation: str

class EHRDetectionRequest(BaseModel):
    conversation: str

ehr_router = APIRouter(prefix="/ehr")

@ehr_router.post("/request")
async def ehr_function(request: EHRRequest) -> Dict[str, Any]:
    try:
        query = request.query

        response = openai_ehr_controller.openai_ehr_controller(context={"name": "Daniel", "emotion": "happy"}, query=query)

        print("Response:", response)

        if not response:
            return {"status": 404, "message": "No response generated"}
        
        tts_class = tts_controller.TTSController()

        tts_class.convert_text_to_speech(response, request.voice_repo)

        return {"status": 200, "characterized_response": response, "voice": request.character}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@ehr_router.post("/check")
async def ehr_check(request: EHRCheckRequest) -> Dict[str, Any]:
    try:
        checklist = request.checklist
        conversation = request.conversation

        response = openai_checklist_controller.openai_checklist_controller(conversation, checklist)

        print("Response:", response)

        return {"status": 200, "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@ehr_router.post("/detection")
async def ehr_detection(request: EHRDetectionRequest) -> Dict[str, Any]:
    try:
        conversation = request.conversation

        response = openai_detection_controller.openai_detection_controller(conversation)

        print("Response:", response)

        return {"status": 200, "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))