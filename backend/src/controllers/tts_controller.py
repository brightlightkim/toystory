import requests
import json
import os
from fastapi import HTTPException

class TTSController:
    def __init__(self):
        self.api_key = os.getenv("PLAYHT_API_KEY")
        self.user_id = os.getenv("PLAYHT_USER_ID")
        self.base_url = "https://api.play.ht/api/v2/"

    def convert_text_to_speech(self, text, voice):
        headers = {
            "AUTHORIZATION": f"Bearer {self.api_key}",
            "X-User-Id": os.getenv("PLAYHT_USER_ID"),
            "accept": "audio/mpeg",
            "content-type": "application/json"
        }

        print("Headers", headers)

        data = {
            "text": text,
            "voice": voice,
            "output_format": "mp3",
            "voice_engine": "PlayDialog",
        }

        print("Data", data)

        response = requests.post(f"{self.base_url}tts/stream", headers=headers, data=json.dumps(data))

        print("Response", response.text)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to convert text to speech")

        return response.content  # Return binary audio content instead of JSON

    def get_speech(self, transcription_id):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-User-ID": self.user_id
        }

        response = requests.get(f"{self.base_url}transcription/{transcription_id}", headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get speech")

        return response.json()