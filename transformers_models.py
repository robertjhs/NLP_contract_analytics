import os
import sys
import warnings
import pandas as pd

import transformers
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

if not sys.warnoptions:
    warnings.simplefilter("ignore")

transformers.logging.set_verbosity_error()

# read file names and contracts from a given folder
def read_contracts(folder):
    files = []
    contracts = []
    for file in os.listdir(folder):
        fullpath = folder + '/' + file
        with open(fullpath) as f:
            contracts.append(f.read())
            files.append(fullpath)
    return files, contracts


# read a single text file
def read_text(filename):
    with open(filename) as f:
        text = f.read()
    return text

# format output results with model description
def format_results(list,model_desc):
    summary = next(iter(list[0].values()))
    result = '\n' + model_desc + ':\n\n' + summary + '\n'
    return result


# read text from a folder
# folder = './Desktop/Galvanize/projects/NLP_contract_analytics/data/full_contract_txt'
# files, contracts = read_contracts(folder)
# text = read_text(files[1])

'''
SAMPLE TEXTS
'''
text = [
'''
EXHIBIT 10.17

                        TRANSPORTATION SERVICE AGREEMENT                          UNDER RATE SCHEDULE FTS OR ITS

         THIS AGREEMENT ("Agreement"), entered into on May 20, 1992, is between Arkansas Western Pipeline Company ("Transporter"), an Arkansas corporation, and Associated Natural Gas Company, a division of Arkansas Western Gas Company, ("Shipper");

                                  WITNESSETH:

         WHEREAS, Shipper has requested natural gas for that Transporter transport Shipper; and

         WHEREAS, Transporter has agreed to provide such transportation for Shipper subject to the terms and conditions set forth in this Agreement.

         NOW, THEREFORE, in consideration of the promises and the mutual covenants herein contained, the parties agree as follows:

''',

'''
EXHIBIT 10.17

                        TRANSPORTATION SERVICE AGREEMENT                          UNDER RATE SCHEDULE FTS OR ITS

         THIS AGREEMENT ("Agreement"), entered into on May 20, 1992, is between Arkansas Western Pipeline Company ("Transporter"), an Arkansas corporation, and Associated Natural Gas Company, a division of Arkansas Western Gas Company, ("Shipper");

                                  WITNESSETH:

         WHEREAS, Shipper has requested natural gas for that Transporter transport Shipper; and

         WHEREAS, Transporter has agreed to provide such transportation for Shipper subject to the terms and conditions set forth in this Agreement.

         NOW, THEREFORE, in consideration of the promises and the mutual covenants herein contained, the parties agree as follows:

                                   ARTICLE I

                                  DEFINITIONS

         1.1      "Maximum Daily Delivery Obligation (MDDO)" means the maximum                   daily quantity of natural gas, expressed in Dekatherms (Dth),                   that Transporter is obligated to deliver from time to time at                   the Point(s) of Delivery specified in Exhibit B to the                   executed Agreement.

         1.2      "Maximum Daily Quantity (MDQ) " means the maximum daily                   quantity of natural gas, expressed* in Dth's, that Transporter                   is obligated under the executed Agreement to transport on                   behalf of' Shipper, which shall be 23,000 Dth.

         1.3      "Equivalent Quantity" means the quantity, expressed in Dth's,                   delivered to Shipper by Transporter at the Point(s) of                   Delivery. Such quantity is equal to the quantity of gas                   received from Shipper at the Point(s) of Receipt less Fuel                   Usage and Applicable Shrinkage.

         1.4      "Fuel Usage and Applicable Shrinkage" means the quantity of                   natural gas retained by Transporter for fuel usage, leakage,                   blow-down, minor line pack fluctuations, and lost and                   unaccounted for natural gas.

'''
]

'''
SUMMARIZATION with Huggingface Transformers

# summarization | Bart model with Pytorch
summarizer_pyt = pipeline("summarization")
summary_pyt = summarizer_pyt(text[0], min_length=5, max_length=100)

# summarization | t5-base model with TensorFlow
summarizer_tf = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
summary_tf = summarizer_tf(text[0], min_length=5, max_length=100)


print(format_results(summary_pyt, 'Summary by Bart model with Pytorch'))
print(format_results(summary_tf, 'Summary by t5-base model with TensorFlow'))
'''

'''
ENTITY EXTRACTION with Huggingface Transformers
'''
# convert results to a Pandas dataframe
def ner_categories(ner):
    df = pd.DataFrame(ner)
    df.drop(['start','end'], axis=1, inplace=True)
    df.sort_values('score', ascending=False)
    return df

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

ner_results = nlp(text[0])
print(ner_categories(ner_results))