from openai import OpenAI
import os


def openai_chat_controller(sessionId: str, style: str, content: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if style == "donald":
        style = "trump"

        prompt = (
            """
			<direction>
				You are a highly skilled counselor. You should analyze what patient says and answer them.
			</direction>
			<context>"""
            + f"This is what the patient says: {content}."
            + """If the patient discusses highly emotional or sensitive topics, return "RAG" in the type parameter in the output. It will be used later for the RAG(Retrieval Augmented Generation) logic. and "NORAG" otherwise.
				These words can be classified as 'RAG': ["die", "sad", "depression", "angry", "kill", "addiction", "divorce", "smoke", "drink", etc]
			</context>"""
            + """
			<output>
				{{
					"script": "Generate a repsonse in and the tone and personality of the """
            + f"specified character: {style}"
            + """, "original_script": The original text provided by the user.
					"voice": "trump" | "elon" | "ted the bear"
				}}
			</output>
			<example output1>
				{
					"script": "Ladies and gentlemen, we're embarking on a tremendous journey to restore our nation's greatness. Our economy is booming like never before, jobs are coming back, and we're putting America first. Together, we'll make our country stronger, safer, and more prosperous than ever. Believe me, the best is yet to come.",
					"original_script":  "Ladies and gentlemen, we are beginning an important journey to rebuild our nation's strength. The economy is growing, jobs are increasing, and we are prioritizing our country. By working together, we will make our nation more secure, resilient, and successful. The future holds great promise.", 
					"voice": " "
				}
			</example output1>
			<example output2>
			{
				"script": "My fellow citizens, we are launching an incredible movement to bring our country back to glory. Businesses are thriving, wages are rising, and we're putting our people first. Together, we're making history—stronger, safer, and more successful than ever before. Believe me, the best days are ahead.",
				"original_script": "Dear citizens, we are starting a significant effort to strengthen our nation. Companies are growing, incomes are improving, and we are prioritizing our communities. By uniting, we will build a brighter, safer, and more prosperous future for everyone."
				"voice": "elon"
			}
			</example output2>
		"""
        )

    history = [
        {"role": "user", "content": prompt},
    ]

    # check for previous conversation with the ai with the same user and session
    # supabase = create_client(supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_KEY"))

    # supabase.postgrest.table("ChatHistory").insert({
    # 	"session_id": sessionId,
    # 	"content": json.dumps({ "role": "user", "content": prompt}),
    # 	"style": style,
    # }).execute()

    # response = supabase.postgrest.from_table("ChatHistory").select("*").eq("session_id", sessionId).execute()
    # print("what is this?"+response)

    # if response.data:
    # 	for item in response.data:
    # 		history.append(json.loads(item["content"]))
    # history.append(json.loads(response.data[0]["content"]))

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
    )

    print("Response: ", result.choices[0].message.content)

    # if result.choices[0].message:
    # 	supabase.postgrest.table("ChatHistory").upsert({
    # 		"session_id": sessionId,
    # 		"content": json.dumps({ "role": result.choices[0].message.role, "content": result.choices[0].message.content}),
    # 		"style": style,
    # 	}).execute()

    return result.choices[0].message.content
