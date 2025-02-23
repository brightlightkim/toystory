from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.controllers.openai_emotion_controller import openai_emotion_controller
import numpy as np
import cv2
import base64
import aiohttp
import io

emotion_router = APIRouter(prefix="/emotion")

WINDOW_SIZE = 10
DECAY_FACTOR = 0.8


class ImageRequest(BaseModel):
    image_url: str


@emotion_router.post("/analyze")
async def analyze(request: ImageRequest):
    """
    Get the image from URL and analyze the emotion of the face
    """
    emotion_data = openai_emotion_controller(request.image_url)

    if isinstance(emotion_data, list) and len(emotion_data) > 0:
        emotion_data = emotion_data[0]

    # Extract the emotion and happiness score
    emotion = emotion_data.get("emotion", "neutral")
    happiness_score = float(emotion_data.get("happiness_score", 0))

    return JSONResponse(
        content={
            "emotion": emotion,
            "happiness_score": round(float(happiness_score), 2),
        }
    )


@emotion_router.get("/analyze_robot/")
async def analyze_robot_image():
    return JSONResponse(content={"emotion": "No image found", "happiness_score": 0})


@emotion_router.get("/happiness_score/")
async def get_happiness_score():
    """
    현재까지의 평균 행복지수를 반환하는 API
    """

    session_emotions = []

    if not session_emotions:
        return JSONResponse(content={"happiness_score": 0})

    average_score = sum(session_emotions) / len(session_emotions)
    return JSONResponse(content={"happiness_score": round(float(average_score), 2)})
