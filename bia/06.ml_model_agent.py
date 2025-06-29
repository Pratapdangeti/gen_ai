


from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_experimental.tools import PythonAstREPLTool

from langchain_openai import ChatOpenAI
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

import openai
import json

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)
openai.api_key = open_ai_details['openai_api_key']


# Train a sample model
df = pd.DataFrame({
    'X': np.arange(10),
    'y': np.arange(10) * 2 + 1
})
X = df[['X']]
y = df['y']
model = LinearRegression()
model.fit(X, y)

# Inject the model and df into the Python REPL tool
repl_tool = PythonAstREPLTool(locals={"model": model, "df": df})

# Define tools
tools = [repl_tool]

# Create LLM
llm = ChatOpenAI(openai_api_key = openai.api_key,temperature=0)


# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  
    verbose=True
)


# Example query
response = agent.run("Predict the y value for X = 15 using the model.")
print(response)

# Printing model coefficients & intercept
print(agent.run("print details of the model.intercept_ & model.coef_"))



print("Completed")

