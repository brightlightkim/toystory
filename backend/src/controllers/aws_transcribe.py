from fastapi import FastAPI, HTTPException
import boto3
import time
import requests


def transcribe_audio(job_name, job_uri, media_format, language_code):
    # Initialize the Boto3 client for Transcribe
    transcribe_client = boto3.client('transcribe', region_name='us-east-1')  # Change the region as needed

    # Start the transcription job
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=media_format,
        LanguageCode=language_code
    )

    # Check the status of the transcription job
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print(f"Job status: {job_status}")
        time.sleep(5)

    # If the job is completed, get the transcript URL
    if job_status == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript_response = requests.get(transcript_uri)
        transcript_data = transcript_response.json()
        return transcript_data
    else:
        raise HTTPException(status_code=500, detail="Transcription job failed")
