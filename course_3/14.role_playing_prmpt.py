import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


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



#Example 1:
system_prompt_1 = """Act as an expert financial analyst"""
user_prompt_1 = """Offer insights into retirement planning for 
individuals approaching retirement age."""

print(get_response(system_prompt=system_prompt_1,user_prompt=user_prompt_1))


#Example 2:
system_prompt_2 = """Act as a seasoned technology journalist coverign the latest
trends in the tech industry. You're known for your thorough reasearch and insightful
analysis."""

user_prompt_2 = """What is the impact of Artificial Intelligence on job markets?"""

print(get_response(system_prompt=system_prompt_2,user_prompt=user_prompt_2))


#Example 3:
system_prompt_3 = """Act as a seasoned technology jouralist covering the latest trends
in the tech industry. You've known for your in-depth research and insightful analysis.
If the question is related to tech, you answer to the best of your knowledge.
Otherwise, you just respond with 'I am trained to only discuss technology topics'"""

user_prompt_3 = """Which Americal literature books do you recommend?"""

print(get_response(system_prompt=system_prompt_3, user_prompt=user_prompt_3))





print("Completed")
