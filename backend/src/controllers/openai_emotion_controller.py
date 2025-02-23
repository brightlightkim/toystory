from openai import OpenAI
import os
import base64
from io import BytesIO
import json

def openai_emotion_controller(image_base64: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Here is the image of the person."},
        {"role": "user", "content": image_base64},
    ]

    for _ in range(3):
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
        )

        response_content = result.choices[0].message.content.strip()

        try:
            response_json = json.loads(response_content)
            if "emotion" in response_json and "happiness_score" in response_json:
                return response_json
        except json.JSONDecodeError:
            pass

        history.append({"role": "assistant", "content": response_content})
        history.append({"role": "user", "content": "Please provide the result as a JSON object with 'emotion' and 'happiness_score' keys."})

    return {"emotion": "unknown", "happiness_score": 0}
