import requests
import json
import os
import time

from dotenv import load_dotenv

from supabase import create_client, Client
from fastapi import HTTPException

from fastapi import HTTPException

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


class TTSController:
    def __init__(self):
        self.api_key = os.getenv("PLAYHT_API_KEY")
        self.user_id = os.getenv("PLAYHT_USER_ID")
        self.base_url = "https://api.play.ht/api/v2/"

    def convert_text_to_speech(self, text, voice):
        try:
            authorization = f"Bearer {self.api_key}"
            print("Authorization", authorization)
            user_id = os.getenv("PLAYHT_USER_ID")
            print("User ID", user_id)
            payload = {
                "voice": voice,
                "output_format": "mp3",
                "voice_engine": "PlayHT2.0-turbo",
                "text": text
            }
            headers = {
                "accept": "audio/mpeg",
                "content-type": "application/json",
                "AUTHORIZATION": authorization,
                "X-USER-ID": user_id,
            }

            response = requests.post(
                "https://api.play.ht/api/v2/tts/stream", headers=headers, data=json.dumps(payload)
            )

            if response.status_code == 200:
                # Generate a unique filename
                filename = f"audio_{int(time.time())}.mp3"

                # Save the audio content to a temporary file
                with open(filename, "wb") as f:
                    f.write(response.content)

                # Upload to Supabase storage
                with open(filename, "rb") as f:
                    supabase.storage.from_("robot").upload(
                        file=f,
                        path=f"audio/{filename}",
                        file_options={"content-type": "audio/mpeg"},
                    )

                # Clean up the temporary file
                os.remove(filename)

                # Return the Supabase storage URL
                file_url = supabase.storage.from_("robot").get_public_url(
                    f"audio/{filename}"
                )
                return file_url

            print("Response Content", response.content)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to convert text to speech",
                )

            return response.content
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, detail=f"Failed to convert text to speech: {e}"
            )

    def get_speech(self, transcription_id):
        headers = {"Authorization": f"Bearer {self.api_key}", "X-User-ID": self.user_id}

        response = requests.get(
            f"{self.base_url}transcription/{transcription_id}", headers=headers
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Failed to get speech"
            )

        return response.json()
