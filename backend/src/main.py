from fastapi import FastAPI

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.openai import openai_router
from routes.sst import sst_router
from routes.tts_routes import tts_router  
# from routes.emotion import emotion_router
from routes.final import final_router

# 현재 파일의 디렉토리를 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), '.env')

load_dotenv()

app = FastAPI()

app.include_router(openai_router)
app.include_router(sst_router)
app.include_router(tts_router)
app.include_router(final_router)

# CORS 설정 (React 프론트엔드 연결)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)