


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


#zero-shot prompting
zero_shot_prompt = """What is prompt engineering?"""

print(get_response(zero_shot_prompt))


#one-shot prompting

one_shot_prompting="""
Q: Sum the numbers 3, 5, and 6. A: 3+5+6 = 14
Q: Sum the numbers 2, 4, and 7. A:
"""

print(get_response(one_shot_prompting))


one_shot_prompting_v2="""
Q: Sum the numbers 3, 5, and 6. A: The sum of 3, 5, and 6 is 14
Q: Sum the numbers 2, 4, and 7. A:
"""

print(get_response(one_shot_prompting_v2))


#Few-shot prompting
few_sht_prompt = """
Text: Today the weather is fantastic -> Classification: positive
Text: The furniture is small -> Classification: neutral
Text: I don't like  your attitude -> Classification: negative
Text: That shot selection was awful -> Classification: 
"""

print(get_response(few_sht_prompt))

#few-shot prompting example 2
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user",
               "content":"Today the weather is fantastic"},
              {"role":"assistant",
               "content":"positive"},
              {"role":"user",
               "content":"I don't like your attitude"},
              {"role":"assistant",
               "content":"negative"},
               {"role":"user",
                "content":"That shot selection was awful"},
                {"role":"assistant","content":""}
    ],
    temperature=1
)

print(response.choices[0].message.content)




print("Completed")