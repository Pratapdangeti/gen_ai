




import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user",
                   "content":prompt}],
        temperature=0)
    print("\n")
    return response.choices[0].message.content


#Multi-step prompting
prompt = """Compose a travel blog as follows:
Step 1: Introduce the destination
Step 2: Share personal adventures during the trip
Step 3: Summarize the journey
"""
print(get_response(prompt=prompt))



#Analyzing solution correctness
calculator = """
def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
"""

# single-step prompt
prompt = f"""Determine if the code delimited by triple backticks is correct or not.
Answer by yes or no.
```{calculator}```
"""
print(get_response(prompt=prompt))



#Multi-step prompt
mstep_prompt = f"""Determine the correctness of the code delimited by triple backticks as follows:
Step 1: Check the code correctness in each function.
Step 2: Verify if the divide function handles the case when dividin by 0.
Code: ```{calculator}```
"""

print(get_response(prompt=mstep_prompt))



print("Completed")
