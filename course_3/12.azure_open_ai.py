


import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)


# Required configuration for Azure OpenAI
openai.api_type = "azure"
openai.api_base = "https://pratap-azoai.openai.azure.com/"  
openai.api_version = "2024-02-01" 
openai.api_key = open_ai_details['azure_openai_api_key'] 

deployment_name = "gpt-35-turbo"  

client = openai.AzureOpenAI(
    api_key = openai.api_key,
    api_version = openai.api_version, 
    azure_endpoint = openai.api_base 
)


# Prompt examples
examples = """
Input: [150000, 180000, 200000, 170000] -> Output: 175000.0,
Input: [10000, 25000, 30000, 15000] -> Output: 20000.0,
Input: [50000, 75000, 60000, 45000] -> Output: 57500.0
"""
prompt_e = f"""You are provided with input-output examples delimited by triple backlists
for a Python program that receives a list of quarterly sales data. Write code 
for this program.
```{examples}```
"""

response = client.chat.completions.create(
    model=deployment_name,  
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_e}

        # {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]
)


print(response.choices[0].message.content)



print("Completed")