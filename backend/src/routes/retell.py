from fastapi import APIRouter
from pydantic import BaseModel

import sys

sys.path.append("..")
from controllers.retell_phone_agent import call_ted_the_bear


class PromptRequest(BaseModel):
    delay: int = 30


openai_router = APIRouter(prefix="/chat")


@openai_router.post("/")
def call_agent(request: PromptRequest):

    try:
        call_ted_the_bear(request.delay)
        return {"status": 200, "message": "Call initiated!"}
    except Exception as e:
        return {"status": 500, "message": str(e)}
