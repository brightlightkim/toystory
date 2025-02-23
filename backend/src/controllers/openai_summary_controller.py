from openai import OpenAI
import os


def openai_summary_controller(conversation: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = "You are an experienced doctor who is summarizing a conversation with a young patient in a clinical context."

    system_prompt = system_prompt.format(
        conversation=conversation
    )

    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Summarize the conversation and offer a follow-up to the patient. Answer ONLY in plaintext and only what is necessary. Here is the conversation: " + conversation},
    ]

    result = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
    )

    response_content = result.choices[0].message.content
    return response_content
