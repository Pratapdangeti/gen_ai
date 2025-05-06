

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


# Summarizing text
text = f"""I recently purchased your XYZ Smart Watch and wanted to provide some feedback
based on my experience with the product. I must say that I'm impressed with the sleek design
and build quality of the watch. It feels comfortable on the wrist and looks great with any
outfit. The touchscreen is responsive and easy to navigate through the various features.
"""
prompt_t = f"""Summarize the text delimited by triple backticks:
```{text}```
"""

print(get_response(prompt=prompt_t))


# Effective prompt: output limits 
prompt_os = f"""Summarize the text delimited by triple backticks in one sentence:
```{text}```
"""

print(get_response(prompt=prompt_os))



# Output structure
prompt_os_struct = f"""Summarize the text delimited by triple backticks, in at most
three bullet points.
```{text}```
"""
print(get_response(prompt=prompt_os_struct))


# Model to focus on specific parts of text
prompt_spart_text = f"""Summarize the review delimited by triple backticks, in three
sentences, focusing on the key features and user experience:
```{text}```
"""

print(get_response(prompt=prompt_spart_text))


#### Text Expansion
service_description = """Service: Social XYZ
- Social Media Strategy Development
- Content Creation and Posting
- Audience Engagement and Community Building
- Increased Brand Visibility
- Enhanced Customer Engagement
- Data-Driven Marketing Decisions
"""
prompt_te = f"""Expand the description for the Social XYZ service delimited by
triple backticks to provide an overview of its features and benefits, without bypassing
the limit of two sentences. Use a professional tone.
```{service_description}```
"""

print(get_response(prompt=prompt_te))




print("Completed")
