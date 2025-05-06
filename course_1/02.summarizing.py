


import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI

client = OpenAI(api_key=openai.api_key)

#Text editing
prompt = """
Update name to Marteen, pronouns to he/him, and job title to Senior Content Developer 
in the following text:

Joanne is a Content Developer at DataCamp. Her favorite programming language is R,
which she uses for her statistical analyses.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user","content":prompt}]
)

print("\n\n")
print(response.choices[0].message.content)


# text summarization
text = """
Customer: Hi, I'm trying to log into my account, but it keeps saying my password is incorrect.
I'm sure I'm entering the right one.

Support: I'm sorry to hear that! Have you tried resetting your password?
...
"""


prompt_2 = f"""Summarize the customer support chat in three concise key points: {text} """

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt_2}]
)

print("\n\n")
print(response.choices[0].message.content)



# Controlling response length
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user",
               "content":"Write a haiku about AI."}],
    max_completion_tokens=5
)
print("\n\n")
print(response.choices[0].message.content)


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user",
               "content":"Write a haiku about AI."}],
    max_completion_tokens=30
)
print("\n\n")
print(response.choices[0].message.content)


# Calculating the cost
max_completion_tokens=30

input_token_price = 0.15/1_000_000
output_token_price = 0.6/1_000_000

input_tokens = response.usage.prompt_tokens
output_tokens = max_completion_tokens


#Calculate cost
cost = (input_tokens * input_token_price + output_tokens * output_token_price)

print(f"Estimated cost: ${cost}")



print("Completed")