
import pandas as pd

from pandasai.llm import OpenAI
from pandasai.schemas.df_config import Config
from pandasai import SmartDataframe

import openai
import json

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)
openai.api_key = open_ai_details['openai_api_key']

#Importing data frames
df = pd.read_csv("D:\\Projects\\Forecasting\\misc\\bia\\all-states-history.csv")


smart_df = SmartDataframe(df=df, config=Config(llm=OpenAI(api_token = openai.api_key)))

print(smart_df.chat("what is the treand of deaths for the state AK over the period? "))

# print(smart_df.chat("what is this dataset is talking about? "))

# print(smart_df.chat("what is median alcohol value? "))

# print(smart_df.chat("what are 25th, 50th and 75th percentiles of alcohol value? "))





print("Completed")
