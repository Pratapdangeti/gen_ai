



import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


def create_article_text(article):
    return f"""Headline: {article['headline']}
    Topic: {article['topic']}   
    Keywords: {', '.join(article['keywords'])}"""


articles =[
    {"headline":"Economic Growth Continues Amid Global Uncertainity","topic":"Business"},
    {"headline":"Interest rates fall to historic lows","topic":"Business"},
    {"headline":"Scientists Make Breakthrough Discovery in Renewable Energy","topic":"Science"},
    {"headline":"India Successfully Lands Near Moon's South Pole","topic":"Science"},
    {"headline":"New Particle Discovered at CERN","topic":"Science"},
    {"headline":"Tech Company Launches Innovative Product to Improve Online Accessibility","topic":"Tech"},
    {"headline":"Tech Giant Buys 49% Stake in AI Startup","topic":"Tech"},
    {"headline":"New Social Media Platform Has Everyone Talking!","topic":"Tech"},
    {"headline":"The Blues get prompted on the final day of the season!","topic":"Sport"},
    {"headline":"1.5 Billion Tune-in to the World Cup Final","topic":"Sport"},
]


article_texts = [create_article_text(article) for article in articles]


def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = texts
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]


article_embeddings = create_embeddings(article_texts)

print(article_embeddings)

from scipy.spatial import distance

def find_n_closest(query_vector, embeddings, n=3):
    distances = []
    for index, embedding in enumerate(embeddings):
        dist = distance.cosine(query_vector, embedding)
        distances.append({"distance":dist,"index":index})
    distances_sorted = sorted(distances, key=lambda x:x['distance'])
    return distances_sorted[0:n]


query_text = "AI"
query_vector = create_embeddings(query_text)[0]

hits = find_n_closest(query_vector, article_embeddings)

for hit in hits:
    article = articles[hit['index']]
    print(article['headline'])



print("Completed")
