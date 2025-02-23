from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

last_processed_files = {"image": None, "audio": None}


async def fetch_latest_image_from_supabase(bucket_name="robot", folder_name="images"):
    """
    Bring the latest image from Supabase
    """
    try:
        response = supabase.storage.from_(bucket_name).list(
            folder_name,
            {"limit": 1, "sortBy": {"column": "created_at", "order": "desc"}},
        )

        if response and len(response) > 0:
            file_info = response[0]
            file_name = file_info["name"]

            # ✅ If the previously processed image is the same, return None (to prevent duplicates)
            if last_processed_files["image"] == file_name:
                return None

            # Download the latest image
            file_path = f"{folder_name}/{file_name}"
            signed_url = supabase.storage.from_(bucket_name).create_signed_url(
                file_path, expires_in=3600
            )

            # ✅ If it's a new image, update the last processed file
            last_processed_files["image"] = file_name
            return signed_url["signedURL"]

        return None
    except Exception as e:
        print(f"Error fetching image from Supabase: {e}")
        return None


async def fetch_latest_user_audio_from_supabase(
    bucket_name="robot", folder_name="user_audio"
):
    """
    Bring the latest user_audio from Supabase
    """
    print("Fetching latest audio from Supabase")
    try:
        response = supabase.storage.from_(bucket_name).list(
            folder_name,
            {"limit": 1, "sortBy": {"column": "created_at", "order": "desc"}},
        )

        if response and len(response) > 0:
            file_info = response[0]
            file_name = file_info["name"]

            # ✅ If the previously processed audio is the same, return None (to prevent duplicates)
            if last_processed_files["audio"] == file_name:
                print("No new audio found. Skipping...")
                return None

            # Download the latest audio
            file_path = f"{folder_name}/{file_name}"
            audio_data = supabase.storage.from_(bucket_name).download(file_path)

            # ✅ If it's a new audio, update the last processed file
            last_processed_files["audio"] = file_name
            print(f"Audio fetched: {file_name}")
            return audio_data

        return None
    except Exception as e:
        print(f"Error fetching audio from Supabase: {e}")
        return None


async def fetch_latest_audio_from_supabase(bucket_name="robot", folder_name="audio"):
    """
    Bring the latest audio from Supabase
    """
    print("Fetching latest audio from Supabase")
    try:
        response = supabase.storage.from_(bucket_name).list(
            folder_name,
            {"limit": 1, "sortBy": {"column": "created_at", "order": "desc"}},
        )

        if response and len(response) > 0:
            file_info = response[0]
            file_name = file_info["name"]

            # ✅ If the previously processed audio is the same, return None (to prevent duplicates)
            if last_processed_files["audio"] == file_name:
                print("No new audio found. Skipping...")
                return None

            # Download the latest audio
            file_path = f"{folder_name}/{file_name}"
            audio_data = supabase.storage.from_(bucket_name).download(file_path)

            # ✅ If it's a new audio, update the last processed file
            last_processed_files["audio"] = file_name
            return audio_data

        return None
    except Exception as e:
        print(f"Error fetching audio from Supabase: {e}")
        return None


async def upload_video_to_supabase(
    bucket_name="robot", folder_name="videos", video_file_path="path/to/video.mp4"
):
    """
    Upload the video to Supabase
    """
    print("Uploading video to Supabase")
    try:
        # File name extraction
        file_name = os.path.basename(video_file_path)
        file_path = f"{folder_name}/{file_name}"

        # Upload the video
        with open(video_file_path, "rb") as video_file:
            upload_response = supabase.storage.from_(bucket_name).upload(
                file_path, video_file
            )

        if upload_response:
            print(f"Video uploaded successfully: {file_name}")

            # 🔥 Make a signed url after storing the video
            signed_url_response = supabase.storage.from_(bucket_name).create_signed_url(
                file_path, expires_in=3600
            )

            if signed_url_response:
                signed_url = signed_url_response.get("signedURL")
                return signed_url
            else:
                print("Failed to generate signed URL")
                return None
        else:
            print("Failed to upload video")
            return None

    except Exception as e:
        print(f"Error uploading video to Supabase: {e}")
        return None
