from transformers import Pipeline

print(pipeline('sentiment-analysis')('we love you'))