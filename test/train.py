import os
import pandas as pd
from transformers import pipeline
from src.texts import get_text

question_answerer = pipeline('question-answering')

# read the first contract in the folder to a variable
path = 'data/full_contract_txt/'
context = get_text(path)

question = 'What is the agreement?'

answer = question_answerer(question=question, context=context)

print(f'ORIGINAL TEXT:/n/n{context}')
print(f'ANSWER:/n/n{answer}')

