import boto3
from typing import Dict, Any
import time
import asyncio


async def transcribe_audio(
    job_name: str, job_uri: str, media_format: str, language_code: str
) -> Dict[str, Any]:
    transcribe = boto3.client("transcribe")
    try:
        # Ensure job_name is unique (you might want to add timestamp)
        unique_job_name = f"{job_name}_{int(time.time())}"

        # Make sure we're passing a string URL
        if isinstance(job_uri, dict):
            job_uri = job_uri.get("signedURL", "")

        if not job_uri:
            raise ValueError("Invalid or empty Media URI")

        response = transcribe.start_transcription_job(
            TranscriptionJobName=unique_job_name,
            Media={"MediaFileUri": job_uri},
            MediaFormat=media_format,
            LanguageCode=language_code,
        )

        # Wait for the transcription to complete
        while True:
            status = transcribe.get_transcription_job(
                TranscriptionJobName=unique_job_name
            )
            if status["TranscriptionJob"]["TranscriptionJobStatus"] in [
                "COMPLETED",
                "FAILED",
            ]:
                break
            await asyncio.sleep(1)

        if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            transcript_uri = status["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]
            # You might need to fetch and parse the transcript from the URI
            return {
                "results": {"transcripts": [{"transcript": "Transcription completed"}]}
            }
        else:
            raise Exception("Transcription job failed")

    except Exception as e:
        raise Exception(f"Transcription error: {str(e)}")
