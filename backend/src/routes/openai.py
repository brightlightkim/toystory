from fastapi import APIRouter, Query
from typing import Annotated
from pydantic import BaseModel

import sys
sys.path.append("..")
from controllers.openai_chat_controller import openai_chat_controller

class Prompt(BaseModel):
  content: str

openai_router = APIRouter(prefix="/openai")

# style:
# - ted: default
# - family: family member
# - celeb: celebrity
@openai_router.post("/chat/{sessionId}/{style}")
def openai_chat(sessionId: str, style: str, prompt: Annotated[Prompt, Query()]):
  return openai_chat_controller(sessionId, style, prompt.content)