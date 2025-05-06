

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
               "content":"What is the difference between mutable and immutable objects?"}]
)

# temperature=1
# max_completion_tokens=5

print("\n\n")
print(response.choices[0].message.content)


# Mitigating misuse with system messages
sys_msg = """
You are finance education assistant that helps students study for exams.

If you are asked for specific, real-world financial advise with risk to their finances,
respond with:

I'm sorry, I am not allowed to provide financial advice.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages = [{"role":"system","content":sys_msg},
                {"role":"user",
                 "content":"Which stocks should I invest in?"}]
)

print(response.choices[0].message.content)




print("Completed")
