from openai import OpenAI
import os


def openai_ehr_controller(context: dict, query: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = ''
    with open("../src/templates/ehr_prompt.txt", "r") as file:
        system_prompt = file.read()

    system_prompt = system_prompt.format(
        query=query,
        child_name=context.get("name", "buddy"),
        child_emotion=context.get("emotion", "happy")
    )

    history = [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}]


    result = client.chat.completions.create(
        model="gpt-4o",
        messages=history,
    )

    response_content = result.choices[0].message.content
    return response_content
