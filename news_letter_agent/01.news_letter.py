import os
from dotenv import find_dotenv, load_dotenv
import openai
import json
import requests


from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_community.utilities import GoogleSerperAPIWrapper


openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERPER_API_KEY")

load_dotenv(find_dotenv())

embeddings = OpenAIEmbeddings()


# 1. Serp request to get list of relevant articles
def search_serp(query):
    search = GoogleSerperAPIWrapper(k=20, type="news")
    response_json = search.results(query)

    # print(f"Response=====>, {response_json}")

    return response_json


# _query = "Explain the new updates in Agentic AI domain?"

_query = "Agentic AI updates site:reuters.com OR site:bbc.com OR site:nytimes.com OR site:forbes.com OR site:bloomberg.com"

# ["Reuters", "BBC", "NYTimes", "Forbes", "Bloomberg"]

response_json = search_serp(query=_query)

response_str = json.dumps(response_json)

print(response_str)


print("Completed")
