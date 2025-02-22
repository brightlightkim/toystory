import requests
import json
from fastapi import HTTPException

class TTSController:
    def __init__(self, PlayHT_API_KEY, user_id):
        self.api_key = PlayHT_API_KEY
        self.user_id = user_id
        self.base_url = "https://api.play.ht/api/v1/"

    def convert_text_to_speech(self, text, voice):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-User-ID": self.user_id,
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "voice": voice
        }

        response = requests.post(f"{self.base_url}convert", headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to convert text to speech")

        return response.json()

    def get_speech(self, transcription_id):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-User-ID": self.user_id
        }

        response = requests.get(f"{self.base_url}transcription/{transcription_id}", headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to get speech")

        return response.json()