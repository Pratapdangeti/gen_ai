

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


prompt = """Generate an Excel sheet containing five student names and their grades"""

print(get_response(prompt=prompt))



updated_prompt = """Generate a table that I can copy to Excel, containing
five student names and their grades
"""
print(get_response(prompt=updated_prompt))


# Analyzing the python function
code = """
def calculate_rectangle_area(length, width):
    area = length * width
    return area
"""

# Initial prompt
prompt_i = f"""
Analyze the code delimited by triple backticks with one sentence
```{code}```.
"""
print(get_response(prompt=prompt_i))


# Prompt refinement
prompt_rf = f"""
Analyze the code delimited by triple backticks and provide its programming 
language with one sentence
```{code}```
"""

print(get_response(prompt=prompt_rf))


# Prompt refinement v2
prompt_rf_2 = f"""
For the function delimited by triple backticks, provide in a structured format the following:
- description: one sentence short description
- language: the programming language used
- input: the inputs to the function
- output: the output returned by the function
```{code}```.
"""

print(get_response(prompt=prompt_rf_2))


# Few-shot prompt - initial prompt
prompt_fs_i = """
Clear skies and a gentle breeze. -> Sunny
Heavy rain and thunderstorms expected. -> Rainy
Fresh snowfall with freezing temperatures. ->
"""
print(get_response(prompt=prompt_fs_i))


prompt_fs_i_2 = """
Clear skies and a gentle breeze. -> Sunny
Heavy rain and thunderstorms expected. -> Rainy
The wind of change brought a refreshing breeze to the company's operations. ->
"""
print(get_response(prompt=prompt_fs_i_2))


# Refined prompt
prompt_rs_i_3 = """
Clear skies and a gentle breeze. -> Sunny
Heavy rain and thunderstorms expected. -> Rainy
The political climate in the country was stormy -> Unknown
The wind of change brought a refreshing breeze to the company's operations. ->
"""

print(get_response(prompt=prompt_rs_i_3))





print("Completed")

