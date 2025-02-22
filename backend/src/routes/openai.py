from fastapi import APIRouter, Query
from typing import Annotated
from pydantic import BaseModel

import sys

sys.path.append("..")
from controllers.openai_chat_controller import openai_chat_controller


class PromptRequest(BaseModel):
    prompt: str
    character: str


openai_router = APIRouter(prefix="/chat")


# style:
# - ted: default
# - family: family member
# - celeb: celebrity
@openai_router.post("/")
def openai_chat(request: PromptRequest):
    response = openai_chat_controller(
        character=request.character, prompt=request.prompt
    )
    return {
        "status": 200,
        "response": response,
    }
