from fastapi import APIRouter, Query
from typing import Annotated
from pydantic import BaseModel
from ..controllers import root_controller, openai_chat_controller

class Prompt(BaseModel):
  content: str

openai_router = APIRouter(prefix="/openai")

@openai_router.get("/")
def openai_root():
	return root_controller()

# style:
# - ted: default
# - family: family member
# - celeb: celebrity
@openai_router.post("/chat/{sessionId}/{style}")
def openai_chat(sessionId: str, style: str, prompt: Annotated[Prompt, Query()]):
  return openai_chat_controller(sessionId, style, prompt.content)