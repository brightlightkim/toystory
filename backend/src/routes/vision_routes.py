from fastapi import APIRouter, Response
import cv2

import sys
sys.path.append("..")
from controllers.vision_controller import MoodAnalyzer

vision_router = APIRouter()
mood_analyzer = MoodAnalyzer()

def generate_frames():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        processed_frame, emotion = mood_analyzer.process_frame(frame)

        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@vision_router.get("/video_feed")
async def video_feed():
    return Response(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@vision_router.get("/emotion")
async def get_emotion():
    return {"emotion": "neutral"}  # Placeholder for emotion detection
