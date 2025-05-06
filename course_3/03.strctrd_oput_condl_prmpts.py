

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

# Structured outputs and conditoinal prompts

# table format
prompt="""Generate a table containing 5 movies I should watch if I am an action lover,
with columns for Title and Rating.
"""

print(get_response(prompt=prompt))

# list format
prompt_l = """Generate a list containing the names of the top 5 cities to visit.
"""

print(get_response(prompt=prompt_l))

# structured paragraph
prompt_sp = """Provide a structured paragraph with clear headings and subheadings
about the benefits of regular exercise an overall health and well-being.
"""
print(get_response(prompt_sp))


# custom output format
text = """Once upon a time in a quaint little village, there lived a curious young boy named David. David was [...]
"""
instructions = """You will be provided with a text delimited by triple backticks. Generate a suitable title for it."""

output_format = """Use the following format for the output:
                - Text: <text we want to title>
                - Title: <the generated title>"""

prompt_cstm = instructions + output_format + f"""{text}"""
print(get_response(prompt_cstm))


# conditional prompts
text = "nuvvu yela unnavo cheppu babu"
prompt_condi_prmpt = f"""You will be provided with a text delimited by triple backticks. If the text is written
in English, suggest a suitable title for it. Otherwise, write 'I only understand English'.
```{text}```
"""
print(get_response(prompt_condi_prmpt))


# multiple conditions
text = """In the heart of the forest, sunlight filters through the lush green canopy, creating a tranquil atmosphere [...]"""

prompt_mcds = f"""You will be provided with a text delimited by triple backticks.
If the text is written in English, check if it contains the keyword 'technology'.
If it does, suggest a suitable title for it,  otherwise, write 'Keyword not found'.
It the text is not written in English, replay with 'I only understand English'.

```{text}```
"""
print(get_response(prompt_mcds))






print("Completed")




