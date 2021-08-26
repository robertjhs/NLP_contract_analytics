from transformers import DebertaV2Tokenizer, DebertaV2Model
import torch

tokenizer = DebertaV2Tokenizer.from_pretrained('./models/deberta-v2-xlarge')
model = DebertaV2Model.from_pretrained('./models/deberta-v2-xlarge')

inputs = tokenizer('Hello, my dog is cute', return_tensors='pt')
outputs = model(**inputs)

last_hidden_states = outputs.last_hidden_state

print(outputs)
print(last_hidden_states)