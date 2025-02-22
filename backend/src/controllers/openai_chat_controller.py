from openai import OpenAI
import os
import json


def openai_chat_controller(character: str, prompt: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = (
        f"""
        <direction>
            You are a highly skilled counselor. You should analyze what patient says and answer them sound like a character the user described: {character}.
        </direction>
        <context>"""
        + f"This is what the patient says: {prompt}."
        + """If the patient discusses highly emotional or sensitive topics, return "RAG" in the type parameter in the output. It will be used later for the RAG(Retrieval Augmented Generation) logic. and "NORAG" otherwise.
            Response in a json format with the following fields:
			- script: The generated response.
			- original_script: The original text provided by the user..
			- voice: "trump" | "elon" | "ted" (Choose the character based on the user's input)
			- type: "NORAG" | "RAG" (Choose the type based on the user's input)
            These words can be classified as 'RAG': ["die", "sad", "depression", "angry", "kill", "addiction", "divorce", "smoke", "drink", etc]
        </context>"""
        + """
        <output>
            {
                "script": "Generate a response in and the tone and personality of the """
        + f"specified character: {character}"
        + """, "original_script": The original text provided by the user.
                "voice": "trump" | "elon" | "ted"
                "type": "NORAG" | "RAG"
            }
        </output>
        <example output>
            {
                "script": "Ladies and gentlemen, we're embarking on a tremendous journey to restore our nation's greatness. Our economy is booming like never before, jobs are coming back, and we're putting America first. Together, we'll make our country stronger, safer, and more prosperous than ever. Believe me, the best is yet to come.",
                "original_script":  "Ladies and gentlemen, we are beginning an important journey to rebuild our nation's strength. The economy is growing, jobs are increasing, and we are prioritizing our country. By working together, we will make our nation more secure, resilient, and successful. The future holds great promise.", 
                "voice": "trump",
                "type": "NORAG"
            }
        </example output>
        <example output>
            {
                "script": "My fellow citizens, we are launching an incredible movement to bring our country back to glory. Businesses are thriving, wages are rising, and we're putting our people first. Together, we're making history—stronger, safer, and more successful than ever before. Believe me, the best days are ahead.",
                "original_script": "Dear citizens, we are starting a significant effort to strengthen our nation. Companies are growing, incomes are improving, and we are prioritizing our communities. By uniting, we will build a brighter, safer, and more prosperous future for everyone.",
                "voice": "elon",
                "type": "NORAG"
            }
        </example output>
        <example output>
            {
                "script": "Hello, I'm Ted the Bear. I'm here to help you with your problems. I'm a good listener and I care about you. I want to help you feel better. I'm here to listen to you and help you through this.",
                "original_script": "Hello, I'm here to help you with your problems. I'm a good listener and I care about you. I want to help you feel better. I'm here to listen to you and help you through this.",
                "voice": "ted",
                "type": "NORAG"
            }
        </example output>
        """
    )

    history = [
        {"role": "user", "content": prompt},
    ]
    
    result = client.chat.completions.create(
		model="gpt-4o",
		messages=history,
		response_format={"type": "json_object"},
	)
    
    response_content = result.choices[0].message.content
    response_dict = json.loads(response_content)
    
    return response_dict
