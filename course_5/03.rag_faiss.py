

import openai
import json

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)
openai.api_key = open_ai_details['openai_api_key']

# pdf loader
from langchain_community.document_loaders import PyPDFLoader
# loader = PyPDFLoader('D:\\Projects\\Forecasting\\misc\\bia\\BCA-BCom-BA-BBA.pdf')
# loader = PyPDFLoader('D:\\Projects\\Forecasting\\misc\\bia\\CommoditiesDemystified-en.pdf')
loader = PyPDFLoader('D:\\Projects\\Forecasting\\misc\\bia\\amann_full.pdf')
docs = loader.load()


#Wikipedia loader
# from langchain_community.document_loaders import WikipediaLoader
# docs = WikipediaLoader(query="Cricket",load_max_docs=10).load()
print(len(docs))

# Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
final_documents = text_splitter.split_documents(docs)


#Embeddings 2
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small",api_key = openai.api_key) 

#VectorDB
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

vector_store = FAISS(
    embedding_function=embeddings,
    index=faiss.IndexFlatL2(1536),
    docstore = InMemoryDocstore(),
    index_to_docstore_id= {},
)

vector_store.add_documents(documents=final_documents)

print("Number of vectors in index:", vector_store.index.ntotal)

query = "what is the origin of cricket?"  
results = vector_store.similarity_search(query, k=2)

for i, result in enumerate(results):
    print(f"Result {i+1}:")
    print(result.page_content)



# Prompt Engineering
from langchain import hub
prompt_1 = hub.pull("rlm/rag-prompt")

retriever = vector_store.as_retriever(search_kwargs = {"k":3})

#Chaining
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# from langchain.chat_models.openai import ChatOpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(openai_api_key = openai.api_key)


rag_chain = (
    {"context":retriever | format_docs, "question":RunnablePassthrough()}
    | prompt_1
    | llm
    | StrOutputParser()
)



print(rag_chain.invoke("explain me about cricket origins"))

print(rag_chain.invoke("explain cricket rules"))


print("Completed")


