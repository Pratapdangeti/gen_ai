import os
import json
import pandas as pd

# from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

import os
import openai
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI
import sqlite3

folder_loc = "D:\\Projects\\Forecasting\\text_to_sql_working\\"


# with open("C:\\Users\\DANGETIP\\Project_code\\models\\open_ai_all.json", "r") as file:
#     open_ai_details = json.load(file)

# model_name = "gpt-4.1"

# subscription_key = open_ai_details[model_name]["azure_openai_api_key"]
# api_version = open_ai_details[model_name]["azure_api_version"]
# endpoint = open_ai_details[model_name]["azure_api_endpoint"]

with open(
    "D:\\Projects\\Forecasting\\text_to_sql_working\\data\\columns_format.txt",
    "r",
) as file:
    _prompt_metadata = file.read()


# Structured Output Parser
response_schemas = [
    ResponseSchema(name="sql_query", description="The SQL query to run")
]
sql_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = sql_parser.get_format_instructions()

# Prompt
template = """You are SQL expert in converting plain English into optimized SQL queries.
Your task is to read given question or text starting with a #, and convert into required SQL.
Using step-by-step reasoning, extract the logic and required variables to a map into SQL query.
You may provide either single or multi-join SQL queries from the following 6 tables as required:
customers, campaigns, customer_reviews_complete, interactions, support_tickets, transactions.
Consider relationships and matching key columns between these tables to determine appropriate joins.
You are also provided with 19 example Text-to-SQL mappings as reference. Your generated queries should 
mirror the structure and intent of these examples, particularly with respect to data quality checks.
Return the final SQL query output in SQL format, where:
- Format the SQL query 
- Strip all \n characters at the end of SQL lines.
- Add a semicolon ; at the end of each SQL query to denote termination.

{prompt_metadata_var}

 - text:# {question_var} ?

 {format_instructions_var}
"""

prompt = PromptTemplate(
    input_variables=["prompt_metadata_var", "question_var", "format_instructions_var"],
    template=template,
)

# llm = AzureChatOpenAI(
#     deployment_name=model_name,
#     openai_api_version=api_version,
#     azure_endpoint=endpoint,
#     api_key=subscription_key,
#     temperature=0.3,
#     streaming=True,
# )

llm_model = "gpt-4.1"
llm = ChatOpenAI(temperature=0.3, model=llm_model)


chain = prompt | llm | sql_parser
import streamlit as st


def handle_user_input(user_input):

    # _question = """what are top-selling categories and their review scores for product development and marketing ?"""

    result = chain.invoke(
        input={
            "prompt_metadata_var": _prompt_metadata,
            "question_var": user_input,
            "format_instructions_var": format_instructions,
        }
    )

    sql_query = result["sql_query"]

    conn = sqlite3.connect(os.path.join(folder_loc, "data", "damydb.dbta"))
    # cursor = conn.cursor()

    result = pd.read_sql_query(sql_query, conn)
    # Display user message
    with st.chat_message("user"):
        st.markdown(f"<h5>{user_input}</h5>", unsafe_allow_html=True)

    # Display bot response
    with st.chat_message("assistant"):
        st.code(sql_query, language="sql")

    # Display bot response
    with st.chat_message("assistant"):
        # st.code(sql_query, language="sql")
        st.table(result)

    conn.close()


# Streamlit UI setup
st.markdown(
    "<h1 style='font-size:32px;'>Text 2 SQL Query Generation</h1>",
    unsafe_allow_html=True,
)

if prompt := st.chat_input("Enter your text here to generate SQL:"):
    with st.spinner("Generating SQL, please wait ..."):
        handle_user_input(prompt)
# print(sql_query)


print("Completed")
