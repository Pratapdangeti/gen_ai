from langchain.llms import OpenAI
from pypdf import PdfReader
import pandas as pd
import re
from langchain.prompts import PromptTemplate

import openai
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")


# Extract Info rom PDF file
def get_pdf_text(pdf_doc):
    text=""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Extract data from text
def extracted_data(pages_data):
    template = """Extract all the following values : Invoice ID, DESCRIPTION, Issue Date, 
         UNIT PRICE, AMOUNT, Bill For, From and Terms from: {pages}

        Expected output: remove any dollar symbols {{'Invoice ID': '1001329','DESCRIPTION': 'UNIT PRICE',
        'AMOUNT': '2','Date': '5/4/2023','AMOUNT': '1100.00', 'Bill For': 'james', 'From': 'excel company',
        'Terms': 'pay this now'}}
        """
    prompt_template = PromptTemplate(input_variables=["pages"], template=template)
    llm = OpenAI(temperature=.7)
    full_response=llm(prompt_template.format(pages=pages_data))
    return full_response

# create documents from the uploaded pdfs
def create_docs(user_pdf_list):
    df = pd.DataFrame({'Invoice ID': pd.Series(dtype='int'),
                   'DESCRIPTION': pd.Series(dtype='str'),
                   'Issue Date': pd.Series(dtype='str'),
	              'UNIT PRICE': pd.Series(dtype='str'),
                   'AMOUNT': pd.Series(dtype='int'),
                   'Bill For': pd.Series(dtype='str'),
	                'From': pd.Series(dtype='str'),
                   'Terms': pd.Series(dtype='str')
                    
                    })

    for filename in user_pdf_list:
        
        print(filename)
        raw_data=get_pdf_text(filename)

        llm_extracted_data=extracted_data(raw_data)
        #Adding items to our list - Adding data & its metadata

        # capture one or more of any character, except newline
        pattern = r'{(.+)}' 
        match = re.search(pattern, llm_extracted_data, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            # Converting the extracted text to a dictionary
            data_dict = eval('{' + extracted_text + '}')
            print(data_dict)
            df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
        else:
            print("No match found.")

        print("********************DONE***************")

    df.head()
    return df