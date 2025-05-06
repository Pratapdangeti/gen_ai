


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


# Language translation
text = """XYZ Scooter is a cutting-edge electric scooter designed for urban adventures.
It's sleek design, long-lasting battery, and smart connectivity offer a seamless and
eco-friendly way to navigate city streets
"""

prompt = f"""Translate the English text delimited by triple backticks to French
```{text}```
"""
print(get_response(prompt=prompt))



#If text language is unknown
text_2 = """Das Produkt ist wirklich schon, und der Preis ist fair."""

prompt_lang = f"""Tell me which language is the text delimited by triple
backticks:
```{text_2}```
"""
print(get_response(prompt=prompt_lang))


#Multi-lingual translation
text = """The product combines top quality with a fair price."""
prompt_mlc = f"""Translate the English text delimited by triple backticks
to French, Spanish, and German:
```{text}```
"""

print(get_response(prompt=prompt_mlc))


# Tone adjustment
text = """Hey there! Check out our awesome summer deals! They're
super cool, and you won't want to miss them. Grab 'em now!"""


prompt_tone = f"""Write the text delimited by triple backticks using a formal
and persuasive tone:
```{text}```
"""

print(get_response(prompt=prompt_tone))


# Tone adjustment: specify audience
text = """Our cutting-edge widget employs state-of-the-art microprocessors and
advanced algorithms, delivering unparalleled efficiency and performance for a wide
range of applications."""

prompt = f"""Write the text delimited by triple backticks to be suitable for a non-technical
audience:
```{text}```
"""
print(get_response(prompt=prompt))


# Correct spelling, grammar, and punctuation mistakes
text = """Dear sir, I wanted too discuss a potentiel opportunity for collaboration.
Pls let me know wen you're available"""
prompt_gr = f"""Proofread the text delimited by triple backticks while keeping the original
text structure intact
```{text}```
"""
print(get_response(prompt=prompt_gr))


# Enhance clarity by modifying text structure
prompt = f"""Proofread and restructure the text delimited by triple backticks for enhanced
readability, flow and coherence:
```{text}```
"""
print(get_response(prompt=prompt))



# Multiple transformations
text = """omg, I cant believe how awesome thsi product is! Its like the best thing ever!
You guys gotta try it out!"""
prompt = f"""Transform the text delimited by triple backticks with the following two steps:
Step 1 - Proofread it without changing its structure
Step 2 - Change the tone to be professional
```{text}```
"""

print(get_response(prompt=prompt))



print("Completed")
