from openai import OpenAI
import os


def openai_detection_controller(conversation: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = """
    You are an experienced psychologist who is analyzing a conversation between a caretaker and a young patient.
    Your task is to determine if the patient is behaving in a concerning manner. 
    If the conversation contains any signs of concerning behavior, output True. Otherwise, output False.
    Here are some examples:
    Conversation: 
    Caretaker: How are you feeling today?
    Patient: I feel really sad and hopeless.
    Result: True

    Conversation: 
    Caretaker: Did you enjoy your day?
    Patient: Yes, I had a lot of fun playing with my friends.
    Result: False
    """

    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Conversation: {conversation}\nResult:"},
    ]

    for _ in range(3):
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
        )

        response_content = result.choices[0].message.content.strip()

        if response_content.lower() in ["true", "false"]:
            return response_content.lower() == "true"

        history.append({"role": "assistant", "content": response_content})
        history.append({"role": "user", "content": "Please provide the result as either True or False."})

    return False
