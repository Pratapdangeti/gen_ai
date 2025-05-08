


import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)



response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role":"system",
        "content":"You are an expert data scientist that explains complex concepts in simple terms"},
        {"role":"user",
         "content":"What is prompt engineering?"}
    ]
)

print(response.choices[0].message.content)


# Using function with 2 prompts



def get_response(system_prompt, user_prompt):
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0)
    print("\n")
    return response.choices[0].message.content


system_prompt = """You are a chatbot that answers financial questions.
Your answers should be precise, formal and objective"""

user_prompt = """Who are you ?"""
print(get_response(system_prompt=system_prompt, user_prompt=user_prompt))


user_prompt_2 = """What do you think about cryptocurrencies ?"""
print(get_response(system_prompt=system_prompt, user_prompt=user_prompt_2))


system_prompt_3 = """You are a chatbot that answers financial questions.
Your answers should be precise, formal and objective.
If the question you receive is within the financial field, answre it to the best of your knowledge.
Otherwise, answer with 'Sorry, I only know about finance.'
"""

user_prompt_3 = """How's the weather today?"""
print(get_response(system_prompt=system_prompt_3,user_prompt=user_prompt_3))



print("Completed")