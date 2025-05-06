


import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI

client = OpenAI(api_key=openai.api_key)


prompt = """Generate a powerful tagline for a new electric vehicle
that highlights innovation and sustainability"""

prompt_2 = """Write a compelling product description for the UltraFit Smartwatch.
Highlight its key featues: 10-day batterly life, 24/7 heart rate and sleep
tracking, built-in GPS, water resistance up to 50 meters, and lightweight design.

Use a persuasive and engaging tone to appeal to fitness enthusiasts
and busy professionals.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user","content":prompt_2}],
    temperature=1
)
# :"Life is like a box of chocolates."
print("\n\n")
print(response.choices[0].message.content)




print("Completed")
