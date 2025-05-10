



import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)

# Distance measure
from scipy.spatial import distance
import numpy as np

print(distance.cosine([0,1],[1,0]))


def create_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = texts
    )
    response_dict = response.model_dump()
    return [data['embedding'] for data in response_dict['data']]


print(create_embeddings(["Python is the best!","R is the best!"]))

print(create_embeddings("DataCamp is awesome!")[0])



search_text = "computer"
search_embedding = create_embeddings(search_text)[0]



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


headline_text = [article['headline'] for article in articles]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=headline_text
)

response_dict = response.model_dump()

for i, article in enumerate(articles):
    article['embedding'] = response_dict['data'][i]['embedding']


distances = []

for article in articles:
    dist = distance.cosine(search_embedding, article['embedding'])
    distances.append(dist)

min_dist_ind = np.argmin(distances)
print(articles[min_dist_ind]['headline'])





print("Completed")

