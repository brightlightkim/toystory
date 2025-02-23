from openai import OpenAI
import os
import json


def openai_checklist_controller(conversation: str, health_record: dict) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = """
    You are an experienced doctor who is summarizing a conversation between a robot teddy bear and a young patient in a clinical context.
    Your task is to construct a JSON object with each condition from the checklist pointing to a boolean that shows whether or not that condition was satisfied during the conversation.
    Here are some examples:
    Conversation: 
    Bear: Hey, have you drank 2 liters of water today?
    User: Yep! All the way
    Bear: What about those bananas?
    User: Yuck! No way!
    Checklist: {"physiologicalFunctions": {"hydration": false, "nutrition": false}}
    Result: {"physiologicalFunctions": {"hydration": true, "nutrition": false}}

    Conversation: 
    Bear: Did you finish your homework?
    User: Yes, I did.
    Bear: Did you clean your room?
    User: No, I forgot.
    Checklist: {"academicPerformance": {"cognitiveEngagement": false}, "physiologicalFunctions": {"personalHygiene": false}}
    Result: {"academicPerformance": {"cognitiveEngagement": true}, "physiologicalFunctions": {"personalHygiene": false}}
    """

    checklist = [key for category in health_record.values() for key in category.keys()]

    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Conversation: {conversation}\nChecklist: {checklist}\nResult:"},
    ]

    for _ in range(3):
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
        )

        response_content = result.choices[0].message.content

        try:
            response_json = json.loads(response_content)
            if all(isinstance(response_json.get(item), bool) for item in checklist):
                for category, conditions in health_record.items():
                    for condition in conditions:
                        if condition in response_json:
                            health_record[category][condition] = response_json[condition]
                return health_record
        except json.JSONDecodeError:
            pass

        history.append({"role": "assistant", "content": response_content})
        history.append({"role": "user", "content": "Please provide the result in the correct JSON format."})

    return health_record
