from transformers import BertModel, BertTokenizer
import torch
import numpy as np
from numpy import linalg as LA

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#ROOT = "/content/drive/My Drive/Capstone/Fine tuned model/"

#model = BertModel.from_pretrained(ROOT)
model = BertModel.from_pretrained('bert-base-uncased')


def return_scores(concept1, concept2, type="BERT"):

  input_ids = torch.tensor(tokenizer.encode(concept1)).unsqueeze(0)  # Batch size 1
  outputs = model(input_ids)[0]
  c1_embed = outputs[0][0].detach().numpy() #Get CLS

  input_ids = torch.tensor(tokenizer.encode(concept2)).unsqueeze(0)  # Batch size 1
  outputs = model(input_ids)[0]
  c2_embed = outputs[0][0].detach().numpy() #Get CLS

  v1 = c1_embed
  v2 = c2_embed
  semantic_relatedness = (1 + (v1.dot(v2)) / (LA.norm(v1) * LA.norm(v2) ) )
  semantic_relatedness /= 2

  return semantic_relatedness