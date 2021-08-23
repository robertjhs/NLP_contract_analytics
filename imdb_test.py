import numpy as np
import pandas as pd
from datasets import load_dataset, load_metric
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer


# read in IMDB dataset
raw_datasets = load_dataset("imdb")


# initialize BERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")


# helper funcion to map text to sentences
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


# tokenize dataset
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)


# train/test split with limited and full dataset
small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))
full_train_dataset = tokenized_datasets["train"]
full_eval_dataset = tokenized_datasets["test"]


# define model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)


# training arguments
training_args = TrainingArguments("test_trainer", evaluation_strategy="epoch")


# set up evaluation metrics
metric = load_metric('accuracy')

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


# instantiate trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics
)

# run training
trainer.evaluate()