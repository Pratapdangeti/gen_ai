

import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)

prompt = "What is prompt engineering?"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user",
               "content":prompt}],
    temperature=0
)

print(response.choices[0].message.content)


def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user",
                   "content":prompt}],
        temperature=0
    )
    return response.choices[0].message.content

response_2 = get_response("What is Anaconda?")
print(response_2)

#Prompt improvement
prompt_3 = """What is prompt engineering? Explain it in terms that can be understood by
a 5-year old"""
response_3 = get_response(prompt_3)
print(response_3)






print("Completed")