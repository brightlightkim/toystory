from fastapi import FastAPI

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.openai import openai_router
from routes.tts_routes import tts_router  

# 현재 파일의 디렉토리를 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), '.env')

# .env 파일 로드 시도
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Warning: .env file not found at {env_path}")

app = FastAPI()

app.include_router(openai_router)
app.include_router(tts_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Speech-to-Text API"}

# CORS 설정 (React 프론트엔드 연결)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 특정 도메인으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)