



import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


response = client.embeddings.create(
    model="text-embedding-3-small",
    input="""Embeddings are a numerical representation of text that can be used to
    measure the relatedness between two pieces of text."""
)


response_dict = response.model_dump()
print(response_dict)

# embedding length: 1,536
print(response_dict['data'][0]['embedding'])

# extracting the total tokens
print(response_dict['usage']['total_tokens'])











print("Completed")
