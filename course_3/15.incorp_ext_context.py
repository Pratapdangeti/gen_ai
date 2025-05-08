import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


def get_response(system_prompt, user_prompt):
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0)
    print("\n")
    return response.choices[0].message.content


# later to the date of model trained events
system_prompt_1 = """Act as a financial expert that knows about the latest trends."""
user_prompt_1 = """What are the top financial trends in 2023?"""



print(get_response(system_prompt=system_prompt_1, user_prompt=user_prompt_1))


system_prompt_2 = """Act as a study buddy that helps me with my studies to 
succeed in exams."""

user_prompt_2 = """What is the name of my favorite instructor?"""

print(get_response(system_prompt=system_prompt_2,
                   user_prompt=user_prompt_2))



response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"system",
               "content":"""You are a customer chatbot that responds to user
               in a gentle way"""},
              {"role":"user","content":"What services do you offer?"},
              {"role":"assistant",
               "content":"""We provide services for web application 
               development, mobile app development, and custom software
               solutions."""},
              {"role":"user","content":"""How many services do you have?"""}]
)


print(response.choices[0].message.content)

# System prompt for external context
services = """ABC Tech Solutions, a leading IT company, offers a range of services:
application development, mobile app development, and custom software solutions."""

system_prompt_1 = f"""You are a customer service chatbot that responds to user 
queries in a gentle way. Some information about our services are delimited by
triple backticks.
```{services}```
"""



print("Completed")
