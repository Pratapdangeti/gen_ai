


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


text = f"""I bought your XYZ Smart Watch and wanted to share my positive experience.
Impressed with its sleek design, comfort, and touchscreen usability."""


prompt = f"""Classify the sentiment of the text delimited by triple backticks as positive, negative, or
neutral. Give your answer as a single word:
```{text}```
"""

print(get_response(prompt=prompt))

# Unspecified categories
prompt_us = f"""Classify the sentiment of the text delimited by triple backticks. Give your answer
as a single word.
```{text}```
"""

print(get_response(prompt=prompt_us))



#Multiple classes

prompt_mc = f"""Identify emotions used in this text. Don't use more than 3 emotions.
Format your answer as a list of words separated by commas:
```{text}```
"""

print(get_response(prompt=prompt_mc))


# Entity extraction

text_desc = f"""The XYZ Mobile X200: a sleek 6.5-inch Super AMOLED smartphone with a 48MP triple-camera,
octa-core processor, 5000mAh battery, 5G connectivity, and Android 11 OS. Secure with fingerprint and
facial recognition. 128GB storage, expandable up to 512GB."""


prompt_ee = f"""Identify the following entities from the text delimited by triple backticks
- Product Name
- Display Size
- Camera Resolution
Format the answer as an unordered list.
```{text_desc}```
"""

print(get_response(prompt=prompt_ee))



#Entity extraction with few-shot prompts
ticket_1 = """Hello, I'm Emma Adams. I'd like to ask about my reservation with the code CAR123.
You can reach me at +123456 if needed."""

ticket_2 = """This is Sarah Williams. I would like to request some information regarding my 
upcoming flight with reservation code FLIGHT987. Thank you."""

entities_1= """
* Customer Details
    - Name: Emma Adams
    - Phone: +123456
* Reservation Details
    - Reservation Code: CARS123
"""

entities_2 = """
* Customer Details:
    - Name: Sarah Williams
* Reservation Details:
    - Reservation Code: FLIGHT987
"""


ticket_3 = """Hello, I'm David Brown (CUST123). I need assistance with my reservaton uder the code
HOTEL456. There are some questions and issues related to my upcoming stay that require your attention.
"""

prompt_eef = f"""Text: {ticket_1} -> Entities: {entities_1},
            Text: {ticket_2} -> Entities: {entities_2},
            Text: {ticket_3} -> Entities: """

print(get_response(prompt=prompt_eef))




print("Completed")