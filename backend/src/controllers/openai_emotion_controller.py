from google import genai
from google.genai import types
import os
import json
import base64
import binascii

def openai_emotion_controller(image_base64: bytes) -> dict:
    # Validate if the input is a valid base64 encoded string
    try:
        base64.b64decode(image_base64, validate=True)
    except binascii.Error:
        return {"error": "Invalid base64 payload"}

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    system_prompt = """
    You are an experienced psychologist who is analyzing an image of a person's face.
    Your task is to determine the emotion the person is feeling and provide a happiness score index ranging from -2 to 2.
    The happiness score index should be:
    -2: Very Unhappy
    -1: Unhappy
    0: Neutral
    1: Happy
    2: Very Happy
    Return the result as a JSON object with the keys 'emotion' and 'happiness_score'. Emotion should be one of 'happy', 'sad', 'angry', 'fearful', or 'neutral'.
    For example:
    {
        "emotion": "happy",
        "happiness_score": 1
    }
    """

    history = [
        system_prompt,
        types.Part.from_bytes(data=image_base64, mime_type="image/jpeg"),
    ]

    for _ in range(3):
        result = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=history
        )

        response_content = result.choices[0].message.content.strip()

        # Remove markdown code block indicators if present
        response_content = response_content.strip()
        if response_content.startswith("```json"):
            response_content = response_content[7:]
        if response_content.startswith("```"):
            response_content = response_content[3:]
        if response_content.endswith("```"):
            response_content = response_content[:-3]
        response_content = response_content.strip()

        try:
            response_json = json.loads(response_content)
            if "emotion" in response_json and "happiness_score" in response_json:
                return response_json
        except json.JSONDecodeError:
            pass

        history.append(response_content)
        history.append("Please provide the result in the correct JSON format.")
        
    return {"emotion": "unknown", "happiness_score": 0}
