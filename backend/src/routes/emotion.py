from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
# from src.controllers.yolo_model import detect_faces
# from src.controllers.deepface_model import analyze_emotion
# from src.controllers.image_processor import preprocess_image, crop_face
# from src.controllers.supabase_handler import fetch_latest_image_from_supabase
from src.controllers.openai_emotion_controller import openai_emotion_controller
import numpy as np
import cv2
import base64

emotion_router = APIRouter(prefix="/emotion")

WINDOW_SIZE = 10
DECAY_FACTOR = 0.8

@emotion_router.get("/analyze_robot/")
async def analyze_robot_image():
    # """
    # Bring the latest image from Supabase and analyze the emotion
    # """
    # contents = await fetch_latest_image_from_supabase()

    # if not contents:
    #     return JSONResponse(content={"emotion": "No image found", "happiness_score": 0})

    # img = preprocess_image(contents)

    # faces = detect_faces(img)
    # if not faces:
    #     return JSONResponse(content={"emotion": "No face detected", "happiness_score": 0})

    # face_img = crop_face(img, faces[0])
    # emotion_data = analyze_emotion(face_img)
    
    # if isinstance(emotion_data, list) and len(emotion_data) > 0:
    #     emotion_data = emotion_data[0]
    
    # emotion_scores = {key: float(value) for key, value in emotion_data.get("emotion", {}).items()}

    # current_happiness_score = (
    #     emotion_scores.get("happy", 0) * 2.0 +
    #     emotion_scores.get("neutral", 0) * 1.0 -
    #     emotion_scores.get("sad", 0) * 1.0 -
    #     emotion_scores.get("angry", 0) * 1.2 -
    #     emotion_scores.get("fear", 0) * 1.1
    # )

    # session_emotions = []
    # if session_emotions:
    #     prev_score = session_emotions[-1]
    #     happiness_score = DECAY_FACTOR * prev_score + (1 - DECAY_FACTOR) * current_happiness_score
    # else:
    #     happiness_score = current_happiness_score

    # session_emotions.append(happiness_score)
    # if len(session_emotions) > WINDOW_SIZE:
    #     session_emotions.pop(0)

    # smooth_happiness_score = sum(session_emotions) / len(session_emotions)

    # return JSONResponse(content={"emotion": emotion_data, "happiness_score": round(float(smooth_happiness_score), 2)})
    return JSONResponse(content={"emotion": "No image found", "happiness_score": 0})

@emotion_router.post("/analyze_webcam/")
async def analyze_webcam(image: UploadFile = File(...)):
    """
    Get the image from the webcam and analyze the emotion of the face
    """
    # contents = await image.read()
    # np_arr = np.frombuffer(contents, np.uint8)
    # img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # faces = detect_faces(img)
    # if not faces:
    #     return JSONResponse(content={"emotion": "No face detected", "happiness_score": 0})

    # face_img = crop_face(img, faces[0])  # 첫 번째 얼굴만 감정 분석
    # emotion_data = analyze_emotion(face_img)  # 감정 분석 실행
    
    # # 🔥 DeepFace의 반환 데이터 구조 처리
    # if isinstance(emotion_data, list) and len(emotion_data) > 0:
    #     emotion_data = emotion_data[0]  # 리스트일 경우 첫 번째 결과 사용
    
    # # 감정 점수 추출
    # emotion_scores = {key: float(value) for key, value in emotion_data.get("emotion", {}).items()}
    # # print("✅ Emotion Scores:", emotion_scores)  # 디버깅용 로그

    # # 주요 감정 기반 행복지수 계산
    # current_happiness_score = (
    #     emotion_scores.get("happy", 0) * 2.0 +   # 행복한 감정 비중 ↑
    #     emotion_scores.get("neutral", 0) * 1.0 - # 중립 유지
    #     emotion_scores.get("sad", 0) * 1.0 -     # 슬픔 영향 ↓
    #     emotion_scores.get("angry", 0) * 1.2 -   # 분노 영향 ↓
    #     emotion_scores.get("fear", 0) * 1.1      # 두려움 영향 ↓
    # )
    
    # session_emotions = []

    # if session_emotions:
    #     prev_score = session_emotions[-1]
    #     happiness_score = DECAY_FACTOR * prev_score + (1 - DECAY_FACTOR) * current_happiness_score
    # else:
    #     happiness_score = current_happiness_score

    # # 🔹 최근 10개 값으로 이동 평균 적용 (변동성 최소화)
    # session_emotions.append(happiness_score)
    # if len(session_emotions) > WINDOW_SIZE:
    #     session_emotions.pop(0)

    # smooth_happiness_score = sum(session_emotions) / len(session_emotions)


    # return JSONResponse(content={"emotion": emotion_data, "happiness_score": round(float(happiness_score), 2)})

    contents = await image.read()
    encoded_image = base64.b64encode(contents).decode('utf-8')

    emotion_data = await openai_emotion_controller(encoded_image)

    if isinstance(emotion_data, list) and len(emotion_data) > 0:
        emotion_data = emotion_data[0]

    # Extract the emotion and happiness score
    emotion = emotion_data.get("emotion", "neutral")
    happiness_score = float(emotion_data.get("happiness_score", 0))

    return JSONResponse(content={"emotion": emotion, "happiness_score": round(float(happiness_score), 2)})
    
    # return JSONResponse(content={"emotion": "No face detected", "happiness_score": 0})


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