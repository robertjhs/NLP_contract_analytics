import pandas as pd
import re
from transformers import DebertaV2Tokenizer, DebertaV2ForQuestionAnswering
import torch


filepath = 'local_data/unlabeled_contracts/2020/000019119.txt'

with open(filepath, 'r', encoding="utf-8") as file:
    contract = file.read().replace('\n', '')


# Clean up and pre-process the text.
def pre_process_text(text):
    # Simple replacement for "\n"
    text = text.replace("\n", " ")     
    
    # Simple replacement for "\xa0"
    text = text.replace("\xa0", " ")  
    
    # Simple replacement for "\x0c"
    text = text.replace("\x0c", " ")
    
    # Get rid of multiple dots
    regex = "\ \.\ "
    subst = "."
    text = re.sub(regex, subst, text, 0)
    
    # Get rid of underscores
    regex = "_"
    subst = " "
    text = re.sub(regex, subst, text, 0)
    
    # Get rid of multiple dashes
    regex = "--+"
    subst = " "
    text = re.sub(regex, subst, text, 0)
    
    # Get rid of multiple stars
    regex = "\*+"
    subst = "*"
    text = re.sub(regex, subst, text, 0)
    
    # Get rid of multiple whitespace
    regex = "\ +"
    subst = " "
    text = re.sub(regex, subst, text, 0)
    
    #Strip leading and trailing whitespace
    text = text.strip()
    
    return text

text = pre_process_text(contract)


def get_questions_from_csv():
    df = pd.read_csv("./data/category_descriptions.csv")
    q_dict = {}
    for i in range(df.shape[0]):
        category = df.iloc[i, 0].split("Category: ")[1]
        description = df.iloc[i, 1].split("Description: ")[1]
        q_dict[category.title()] = description
    return q_dict

qtype_dict = get_questions_from_csv()
labels = [l for l in qtype_dict.keys()]
questions = [q for q in qtype_dict.values()]

answers = []


def get_one_pred(question, text):
    inputs = tokenizer(question, text, padding='max_length', truncation='only_second', return_tensors='pt')
    input_ids = inputs["input_ids"].tolist()[0]
    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits
    # Get the most likely beginning of answer with the argmax of the score
    answer_start = torch.argmax(answer_start_scores)
    # Get the most likely end of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer


def pred_all_questions(questions, text):
    answers = []
    for question in questions[0]:
        print(question)
        inputs = tokenizer(question, text, padding='max_length', truncation='only_second', return_tensors='pt')
        input_ids = inputs["input_ids"].tolist()[0]
        outputs = model(**inputs)
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits
        # Get the most likely beginning of answer with the argmax of the score
        answer_start = torch.argmax(answer_start_scores)
        # Get the most likely end of answer with the argmax of the score
        answer_end = torch.argmax(answer_end_scores) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        answers.append(answer)
        print(answer)
        # inputs = input_ids = outputs = answer_start = answer_start_scores = answer_end = answer_end_scores = answer = None
    return answers


def get_all_preds(labels, questions, text, n):
    question = questions[n]
    label = labels[n]
    answers = []
 
    inputs = tokenizer(question, text, padding='max_length', truncation='only_second', return_tensors='pt')
    input_ids = inputs["input_ids"].tolist()[0]
    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits
    for answer_start_score, answer_end_score in zip(answer_start_scores, answer_end_scores):
        answer_start = torch([answer_start_score])
        answer_end = torch([answer_end_score])
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        answers.append(answer)
    return label, answers


tokenizer = DebertaV2Tokenizer.from_pretrained('./models/deberta-v2-xlarge')
model = DebertaV2ForQuestionAnswering.from_pretrained('./models/deberta-v2-xlarge')

answer = get_one_pred(questions[10], text)
print(answer)
    

# for i, question in enumerate(questions):
#     answer = get_one_pred(question, text)
#     print(f'{labels[i]}: {answer}')