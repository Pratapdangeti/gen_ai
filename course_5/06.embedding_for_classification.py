

import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']

import numpy as np
from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = texts,
        # dimensions=512
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]


topics =[
    {'label':'Tech'},
    {'label':'Science'},
    {'label':'Sport'},
    {'label':'Business'}
]

class_descriptions = [topic['label'] for topic in topics]
class_embeddings = create_embeddings(class_descriptions)

article = {"headline":"How NVIDIA GPUs Could Decide Who Wins the AI Race",
           "keywords":["ai","business","computers"]}


def create_article_text(article):
    return f"""Headline: {article['headline']}
    Keywords: {', '.join(article['keywords'])}"""


article_text = create_article_text(article)
article_embeddings = create_embeddings(article_text)[0]


from scipy.spatial import distance

def find_closest(query_vector, embeddings):
    distances = []
    for index, embedding in enumerate(embeddings):
        dist = distance.cosine(query_vector, embedding)
        distances.append({"distance":dist,"index":index})
    return min(distances, key = lambda x:x['distance'])


closest = find_closest(article_embeddings,class_embeddings)

label = topics[closest['index']]['label']
print(label)


# more detailed descriptions
topics = [
    {'label':'Tech', 'description':'A news article about technology'},
    {'label':'Science','description':'A news article about science'},
    {'label':'Sport','description':'A news article about sports'},
    {'label':'Business','description':'A news article about Business'}
]
class_descriptions = [topic['description'] for topic in topics]
class_embeddings = create_embeddings(class_descriptions)

closest = find_closest(article_embeddings,class_embeddings)

label = topics[closest['index']]['label']
print(label)











print("Completed")
