

import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


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



print(articles[:2])

# length of embeddings
print(len(articles[0]['embedding']))

print(len(articles[5]['embedding']))


from sklearn.manifold import TSNE
import numpy as np


embeddings = [article['embedding'] for article in articles]

print(embeddings[0])

tsne = TSNE(n_components=2, perplexity=5)

embeddings_2d = tsne.fit_transform(np.array(embeddings))

import matplotlib.pyplot as plt
plt.scatter(embeddings_2d[:,0],embeddings_2d[:,1])
topics = [article['topic'] for article in articles]
for i, topic in enumerate(topics):
    plt.annotate(topic, (embeddings_2d[i,0], embeddings_2d[i,1]))

plt.show()


print("Completed")

