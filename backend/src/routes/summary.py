import sys
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

sys.path.append("..")
from controllers import openai_summary_controller

class SummaryRequest(BaseModel):
    conversation: str

summary_router = APIRouter(prefix="/summary")

@summary_router.post("/")
async def ehr_function(request: SummaryRequest) -> Dict[str, Any]:
    try:
        conversation = request.conversation

        response = openai_summary_controller(conversation)

        print("Response:", response)

        if not response:
            return {"status": 404, "message": "No response generated"}

        return {"status": 200, "characterized_response": response, "voice": request.character}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))