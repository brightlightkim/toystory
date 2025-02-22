import requests
import json
import os
import time
from dotenv import load_dotenv

from supabase import create_client, Client
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

    def convert_text_to_speech(
        self,
        text,
        voice="s3://voice-cloning-zero-shot/a9cabd69-695e-48a2-a96d-1f237840c7bc/original/manifest.json",
    ):
        headers = {
            "AUTHORIZATION": os.getenv("PLAYHT_API_KEY"),
            "X-USER-ID": os.getenv("PLAYHT_USER_ID"),
            "accept": "audio/mpeg",
            "content-type": "application/json",
        }

        print("Headers", headers)

        data = {
            "text": text,
            "voice": voice,
            "output_format": "mp3",
            "voice_engine": "Play3.0-mini",
        }

        print("Data", data)

        response = requests.post(
            f"{self.base_url}tts/stream", headers=headers, data=json.dumps(data)
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
