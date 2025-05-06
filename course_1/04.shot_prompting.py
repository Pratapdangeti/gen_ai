

import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI

client = OpenAI(api_key=openai.api_key)


# Zero-shot prompting
prompt = """ Classify sentiment as 1-5 (bad-good) in the following statements:
1. Meal was decent, but I've had better.
2. My food was delayed, but drinks were good. 
"""


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user","content":prompt}],
    temperature=1
)

print("\n\n")
print(response.choices[0].message.content)


# temperature=1
# max_completion_tokens=5

#One-shot prompting
prompt_2 = """Classify sentiment as 1-5 (bad-good) in the following statements:
1. The service was very slow -> 1
2. Meal was decent, but I've had better. ->
3. My food was delayed, but drinks were good. ->
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user","content":prompt_2}],
    # temperature=0.3
)

print("\n\n")
print(response.choices[0].message.content)

# Few-shot prompting
prompt_3 = """Classify sentiment as 1-5 (bad-good) in the following statemetns:
1. The service was very slow -> 1
2. The steak was awfully good! -> 5
3. It was ok, no massive compliants. -> 3
4. Meal was decent, but I've had better ->
5. My food was delayed, but drinks were good. ->
"""


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt_3}],
    # temperature=0.3
)

print("\n\n")
print(response.choices[0].message.content)

# General categorization
prompt_gc = """Classify the followign animals as Land, Sea, or Both. You need to think step by step:
1. Blue whale
2. Polar bear
3. Salmon
4. Dog
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt_gc}],
    # temperature=0.3
)

print("\n\n")
print(response.choices[0].message.content)

# Shot prompting
prompt_spmt = """Classify the followign animals as Land, Sea, or Both. You need to think step by step:
1. Zebra = Land
2. Crocodile = Both
3. Blue whale =
4. Polar bear =
5. Salmon =
6. Dog =
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt_spmt}],
    # temperature=0.3
)

print("\n\n")
print(response.choices[0].message.content)



print("Completed")