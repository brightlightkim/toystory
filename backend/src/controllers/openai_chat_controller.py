from openai import OpenAI
import os
import json

max_retries = 3


class InvalidResponseError(Exception):
    pass


def openai_chat_controller(context: dict, prompt: str):
    # expecting context as {name: str, emotion: str, rag_context: list[str]}
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = ""
    with open("../src/templates/main_prompt.txt", "r") as file:
        system_prompt = file.read()

    if context["rag_context"]:
        with open("../src/templates/rag_ending.txt", "r") as file:
            system_prompt += "\n" + file.read()

            rag_context = [i for i in context["rag_context"]][0]
            system_prompt = system_prompt.format(
                child_name=context["name"],
                child_emotion=context["emotion"],
                rag_context="\n".join(rag_context),
            )
    else:
        with open("../src/templates/no_rag_ending.txt", "r") as file:
            system_prompt += "\n" + file.read()
            system_prompt = system_prompt.format(
                child_name=context["name"],
                child_emotion=context["emotion"],
            )

    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    result = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
    )
    
    response_content = result.choices[0].message.content
    
    return response_content

    # retry_count = 0
    # while retry_count < max_retries:
    #     try:
    # result = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=history,
    # )

    #         response_content = result.choices[0].message.content

    #         retry_count += 1

    #     except json.JSONDecodeError:
    #         retry_count += 1
    #         continue

    # raise InvalidResponseError(
    #     "Failed to get valid response after 3 attempts. Response must include 'script', 'original_script', 'voice', and 'type' fields."
    # )
