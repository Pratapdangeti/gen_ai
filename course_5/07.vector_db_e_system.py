

import json
import openai
import os
from openai import OpenAI

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


class MyEmbeddingFunction:
    def __init__(self, model="text-embedding-3-small", dimensions=512, api_key=None):
        self.client = OpenAI(api_key=openai.api_key )
        self.model = model
        self.dimensions = dimensions

    def __call__(self, texts):
        # Ensure input is a list
        if isinstance(texts, str):
            texts = [texts]

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            dimensions=self.dimensions  # optional
        )
        return [record.embedding for record in response.data]


import chromadb

chroma_client = chromadb.PersistentClient(
    path="D:\\Projects\\Forecasting\\misc\\openai_data_camp\\course_5\\data"
)


embedding_fn = MyEmbeddingFunction(
    model="text-embedding-3-small",
    dimensions=1536, 
    api_key=openai.api_key 
)

collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=embedding_fn
)


collection.add(ids=["my-doc"], documents=["This is the source text"])
collection.add(ids=["my-doc-1", "my-doc-2"],
    documents=["This is document 1", "This is document 2"])

collection.add(ids=["my-doc-4", "my-doc-5"],
    documents=["This is document 1", "This is document 2"] )

# Inspect
print("Collections:", chroma_client.list_collections())
print("Document count:", collection.count())

print(collection.peek())
print(collection.peek().keys())
print(collection.peek()['documents'])
print(len(collection.peek()['embeddings']))
print(len(collection.peek()['embeddings'][0]))

# retrieve particular item
print(collection.get(ids=["my-doc-1"]))


# Cost calculation
# Number of tokens
import tiktoken
enc = tiktoken.encoding_for_model("text-embedding-3-small")


total_tokens = sum(len(enc.encode(text)) for text in documents)

cost_per_1k_tokens = 0.00002

print("Total tokens:", total_tokens)
print("Cost:",cost_per_1k_tokens * total_tokens/1000)




print("Completed")
