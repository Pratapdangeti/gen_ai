

import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI

client = OpenAI(api_key=openai.api_key)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"system",
               "content":"You are a Python programming tutor who speaks concisely."},
              {"role":"user",
               "content":"How do you define a Python list?"},
              {"role":"assistant",
               "content":"Lists are defined by enclosing a comma-separated sequence of objects inside square brackets [ ]."},
              {"role":"user",
               "content":"What is the difference between mutable and immutable objects?"}]
)

print("\n\n")
print(response.choices[0].message.content)

print("Completed")
