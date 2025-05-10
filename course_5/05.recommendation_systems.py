



import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']

import numpy as np
from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


articles = [
    {"headline":"Economic Growth Continues Amid Global Uncertainty",
     "topic":"Business",
     "keywords":["economy","business","finance"]},
    {"headline":"1.5 Billion Tune-in to the World Cup Final",
     "topic":"Sport",
     "keywords":["soccer","world cup","tv"]}
]

current_article = {"headline":"How NVIDIA GPUs Could Decide Who Wins the AI Race",
                   "topic":"Tech",
                   "keywords":["ai","business","computers"]}

def create_article_text(article):
    return f"""Headline: {article['headline']}
    Topic: {article['topic']}   
    Keywords: {', '.join(article['keywords'])}"""


article_texts = [create_article_text(article) for article in articles]
current_article_text = create_article_text(current_article)

print(current_article_text)


def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = texts
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]


current_article_embeddings = create_embeddings(current_article_text)[0]
article_embeddings = create_embeddings(article_texts)

from scipy.spatial import distance

def find_n_closest(query_vector, embeddings, n=3):
    distances = []
    for index, embedding in enumerate(embeddings):
        dist = distance.cosine(query_vector, embedding)
        distances.append({"distance":dist,"index":index})
    distances_sorted = sorted(distances, key=lambda x:x['distance'])
    return distances_sorted[0:n]

hits = find_n_closest(current_article_embeddings, article_embeddings)

for hit in hits:
    article = articles[hit['index']]
    print(article['headline'])


# Adding user history
user_history = [
    {"headline":"How NVIDIA GPUs Could Decide Who Wins the AI Race",
     "topic":"Tech",
     "keywords":["ai","business","computers"]},
     {"headline":"Tech Giant Buys 49% Stake In AI Startup",
      "topic":"Tech",
      "keywords":["businesses","AI"]}
]


history_texts = [create_article_text(article) for article in user_history]
history_embeddings = create_embeddings(history_texts)


mean_history_embeddings = np.mean(history_embeddings,axis=0)


articles_filtered = [article for article in articles if article not in user_history]

article_texts = [create_article_text(article) for article in articles_filtered]
article_embeddings = create_embeddings(article_texts)

hits = find_n_closest(mean_history_embeddings, article_embeddings)


for hit in hits:
    article = articles_filtered[hit['index']]
    print(article['headline'])





print("Completed")

