
import json
import openai

with open('D:\\Projects\\Forecasting\\misc\\open_ai.json', 'r') as file:
    open_ai_details = json.load(file)

openai.api_key = open_ai_details['openai_api_key']


from openai import OpenAI
client = OpenAI(api_key=openai.api_key)


def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user",
                   "content":prompt}],
        temperature=0)
    print("\n")
    return response.choices[0].message.content


# Simple prompt
prompt_genc = f"""Write a Python function that accepts a list of quarterly sales, and outputs the average
sales per quarter."""

print(get_response(prompt=prompt_genc))


# Prompt examples
examples = """
Input: [150000, 180000, 200000, 170000] -> Output: 175000.0,
Input: [10000, 25000, 30000, 15000] -> Output: 20000.0,
Input: [50000, 75000, 60000, 45000] -> Output: 57500.0
"""
prompt_e = f"""You are provided with input-output examples delimited by triple backticks
for a Python program that receives a list of quarterly sales data. Write code 
for this program.
```{examples}```
"""

print(get_response(prompt=prompt_e))

#code modification
script = f"""
quarterly_sales = [150, 180, 200, 170]
total_sales = sum(quarterly_sales)
print("Total sales:",total_sales)
"""

prompt_cm = f"""Modify the script delimited by triple backticks to a function that we can
call to compute the total sales given quarterly sales
```{script}```
"""

print(get_response(prompt=prompt_cm))

#interactive
prompt_cm2 = f"""Modify the script delimited by triple backticks as follows:
- Let user input parameters interactively
- Make sure to verify inputs are positive, otherwise, display a message for the user, and ask them
to provide their input again.
```{script}```
"""
print(get_response(prompt=prompt_cm2))


# Code explanation
code = """
def compute_average_sales_per_quarter(quarterly_sales):
    average_sales = sum(quarterly_sales) / len(quarterly_sales)
    return average_sales
"""

prompt_cde = f"""Explain in one sentece what the code delimited by triple backticks does
```{code}```
"""

print(get_response(prompt=prompt_cde))

prompt_cot = f"""Explain what the code delimited by triple backticks does. Let's think step by step.
```{code}```
"""
print(get_response(prompt=prompt_cot))






print("Completed")