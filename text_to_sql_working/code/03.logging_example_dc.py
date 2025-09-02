import os
import json
import logging
import pandas as pd
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

_data_source = "gp-bp-dw-uat.r2r"
folder_path = "C:\\Users\\DANGETIP\\Project_code\\code\\data_catalog\\"

# ----------------- Setup Logging -----------------
log_file = os.path.join(folder_path, "error_log.log")
# log_file = "C:\\Users\\DANGETIP\\Project_code\\code\\data_catalog\\error_log.txt"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

with open("C:\\Users\\DANGETIP\\Project_code\\models\\open_ai_all.json", "r") as file:
    open_ai_details = json.load(file)

model_name = "gpt-4.1"
subscription_key = open_ai_details[model_name]["azure_openai_api_key"]
api_version = open_ai_details[model_name]["azure_api_version"]
endpoint = open_ai_details[model_name]["azure_api_endpoint"]


data = pd.read_csv(
    os.path.join(folder_path, "schema_9580_105_2025-08-12T08-30-54-793865.csv")
)

data["description"] = data["description"].astype("object")
data[["k_key1", "k_key4"]] = data["key"].str.split('"\.', n=1, expand=True)
data["k_key1"] = data["k_key1"].str.replace(r"^\"", "", regex=True)
data[["k_key2", "k_key3"]] = data["k_key4"].str.split(".", n=1, expand=True)

data_3 = data.rename(
    columns={"k_key1": "datasource", "k_key2": "tablename", "k_key3": "colname"}
)

# _table_names = [
#     "vw_dim_customer",
#     "vw_dim_journal_entry",
#     "vw_dim_ptp_bill_of_material_item",
#     "vw_dim_purchase_order",
# ]
_table_names = ["vw_fct_transp_order_execution"]

filtered_df = data_3[(data_3["datasource"] == _data_source)].reset_index(drop=True)

# replace with this for looping over all tables
_total_table_names = filtered_df["tablename"].drop_duplicates().to_list()


# Table to append all procesed dataframes
final_df = pd.DataFrame()
_table_count = 0

for _table_name in _table_names:
    try:
        _req_data = data_3[
            (data_3["datasource"] == _data_source)
            & (data_3["tablename"] == _table_name)
        ]
        _req_data_na = _req_data[_req_data["colname"].isna()].reset_index(drop=True)
        _req_data_notna = _req_data[_req_data["colname"].notna()].reset_index(drop=True)

        _column_schema = "\n".join(
            f"- {row['colname']}: {row['al_datadict_item_column_data_type']}"
            for _, row in _req_data_notna.iterrows()
        )

        llm = AzureChatOpenAI(
            deployment_name=model_name,
            openai_api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
            temperature=0.3,
        )

        class Column(BaseModel):
            name: str = Field(description="column name")
            title: str = Field(description="Meaning of the column")

        class TableSchema(BaseModel):
            columns: List[Column] = Field(
                description="List of columns in the table with their description"
            )

        parser = PydanticOutputParser(pydantic_object=TableSchema)

        # Writing Column titles
        try:
            prompt_template = PromptTemplate(
                template="""
            You are a data cataloging specialist. 
            Analyze the table name and its database metadata containing both column name and column type.

            Table Name: {table_name}

            Columns:
            {column_schema}

            Your task:
            1. Provide a clear, human-readable title for each column. Column names usually consists of multiple words which are separated by _

            2. Consider the global perspective of the table name and other column names while inferring the title.

            Output Rules:
            - Respond ONLY in JSON format
            - No extra text, no markdown, no commentary
            - Follow exactly this schema:
            {format_instructions}
            """,
                input_variables=["table_name", "column_schema"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )

            prompt = prompt_template.format(
                table_name=_table_name, column_schema=_column_schema
            )
            response = llm.invoke(prompt)
            parsed_output = parser.parse(response.content)

            for col in parsed_output.columns:
                _req_data_notna.loc[_req_data_notna["colname"] == col.name, "title"] = (
                    col.title
                )

            logging.info(f"Succesfully written column titles for: {_table_name}")

        except Exception as e:
            print(f"Failed writing column titles for : {_table_name}")
            logging.error(
                f"Failed writing column titles for {_table_name}: {str(e)}",
                exc_info=True,
            )

        # Writing table description
        try:
            prompt_template_desc = PromptTemplate(
                template="""
            You are a data cataloging specialist.

            Analyze the table name and its database metadata, which includes both column names and types.

            Table Name: {table_name}
            Columns:
            {column_schema}

            Your task:
            1. Write a concise 3-4 sentence description of the table's overall purpose and content but write table name in first sentence in a seamless fasion. Focusing on thematic or conceptual details rather than listing individual columns. Combine related columns into broader themes.
            2. Then provide 3-4 questions that this table could help answer.

            Output Rules:
            1. Do not add a "Summary:" heading.
            2. After the summary, insert two HTML line breaks (<br><br>).
            3. Add the heading: "Questions this table might be able to provide answers:<br>".
            4. Place an HTML line break (<br>) after each question.
            5. Ensure the output is plain text, clean, and well-structured.
            """,
                input_variables=["table_name", "column_schema"],
            )

            prompt_desc = prompt_template_desc.format(
                table_name=_table_name, column_schema=_column_schema
            )
            response_desc = llm.invoke(prompt_desc)

            col_idx = _req_data_na.columns.get_loc("description")
            _req_data_na.iloc[0, col_idx] = response_desc.content

            logging.info(f"Succesfully written table description for: {_table_name}")

        except Exception as e:
            print(f"Failed writing table description for: {_table_name}")
            logging.error(
                f"Failed writing table description for {_table_name}: {str(e)}",
                exc_info=True,
            )

        # writing table title
        try:
            prompt_template_table_title = PromptTemplate(
                template="""
            You are a data cataloging specialist. 
            Analyze the table name.

            Table Name: {table_name}

            Your task:
            1. Provide a clear, human-readable title for table name, which usually consists of multiple words which are separated by _

            Output Rules:
            1. Write only the title without "Title:" section title.
            1. Format your response in clean, well-structured plain text.

            """,
                input_variables=["table_name"],
            )

            prompt_table_title = prompt_template_table_title.format(
                table_name=_table_name
            )
            response_table_title = llm.invoke(prompt_table_title)

            col_idx_tt = _req_data_na.columns.get_loc("title")
            _req_data_na.iloc[0, col_idx_tt] = response_table_title.content
            logging.info(f"Succesfully written table title for: {_table_name}")

        except Exception as e:
            print(f"Failed writing table title for : {_table_name}")
            logging.error(
                f"Failed writing table title for {_table_name}: {str(e)}", exc_info=True
            )

        final_df = pd.concat(
            [final_df, _req_data_na, _req_data_notna], ignore_index=True
        )
        logging.info(f"Properly updated table : {_table_name}")

        _table_count += 1
        print(f"table count: {_table_count} ,table name: {_table_name}")

    except Exception as e:
        print(f"No table analyzed for  {_table_name}")
        logging.error(f"Failed analyzing table {_table_name}: {str(e)}", exc_info=True)


# Dropping extra created columns
final_df = final_df.drop(["datasource", "k_key4", "tablename", "colname"], axis=1)

final_df.to_csv(
    os.path.join(folder_path, "data_catalog_sample.csv"),
    index=False,
)


print("Completed")
