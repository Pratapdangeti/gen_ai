

import openai
import json

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)
openai.api_key = open_ai_details['openai_api_key']

#Importing data frames
from sklearn.datasets import load_iris
df = load_iris(as_frame=True)['data']


from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(openai_api_key = openai.api_key)




PROMPT = ("""If you do not know the answer, say you don't know.
          Think step by step.
          Below is the query
          Query: {query} """)

prompt = PromptTemplate(template=PROMPT, input_variables=["query"])

agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=True, allow_dangerous_code=True)


print(agent.run(prompt.format(query = "what is this dataaset about?")))

print(agent.run(prompt.format(query="Plot each column as a barplot!")))

print(agent.run(prompt.format(query="Validate the following hypothesis statistically: petal width and petal length come from the same distribution")))



# Misc
# from langchain_experimental.tools.python.tool import PythonAstREPLTool
# python_tool = PythonAstREPLTool()
# tools = [python_tool]
# python_repl = PythonAstREPLTool()

# from langchain_core.tools import Tool
# Create a Langchain Tool object
# tool = Tool(
#     name="python_repl",
#     description="A Python shell. Use this to execute python commands. Input should be a valid python command.",
#     func=python_repl.run,
# )



print("Completed")