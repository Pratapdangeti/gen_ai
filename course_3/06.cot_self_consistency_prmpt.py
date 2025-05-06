


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


# Standard prompting to solve a reasoning task
propmt = f"""Q: You start with 15 books in your collection. At the bookstore, you purchase 8 new books.
Then, you lend 3 to your friend and 2 to your cousin. Later, you visit another bookstore and 
buy 5 more books. How many books do you have now?
A: The answer is"""

print(get_response(prompt=propmt))



# Chain of thought
propmt_cot = f"""Q: You start with 15 books in your collection. At the bookstore, you purchase 8 new books.
Then, you lend 3 to your friend and 2 to your cousin. Later, you visit another bookstore and 
buy 5 more books. How many books do you have now?
A: Let's think step by step"""

print(get_response(prompt=propmt_cot))


#Chain of thought with few-shots
example = """
Q: The odd numbers in this group add up to an even number: 9, 10, 13, 4, 2.
A: Adding all the odd numbers (9, 13) gives 22. The answer is True.
"""

question = """
Q: The odd numbers in this group add up to an even number: 15, 13, 82, 7.
A:
"""

prompt_cot_fs  = example + question
print(get_response(prompt=prompt_cot_fs))


# Self- consistency prompting
self_consistency_instruction= """Imagine three completely independent experts who reason differently are answering
the question. The final answer is obtained by majority vote. The question is:
"""

problem_to_solve = """If there are 10 cars in the parking lot and 3 more cars arrive. Half the original
number of cars leave. Then, half of the current number of cars arrive. How many cars are there in the parking?
"""

prompt_comb = self_consistency_instruction + problem_to_solve

print(get_response(prompt_comb))





print("Completed")


