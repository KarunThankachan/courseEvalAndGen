import numpy as np
from torchtext import data
from torchtext.vocab import GloVe
from cove import cove
import csv

def return_scores(concept1, concept2, type="GC"):

  concepts = ["concepts", concept1, concept2]
  with open('temp.csv','w') as result_file:
    wr = csv.writer(result_file)
    for concept in concepts:
      wr.writerow([concept,])

  TEXT = data.Field(lower=True, include_lengths=True, batch_first=True)

  train_dataset = data.TabularDataset(
          path="temp.csv", format='csv',
          skip_header = False,
          fields={'concepts':[('concepts',TEXT)]
                  })

  TEXT.build_vocab(train_dataset, vectors=GloVe(name='840B', dim=300, cache='/content/drive/My Drive/nn4nlpdata'))
  outputs_cove_with_glove = cove.MTLSTM(n_vocab=len(TEXT.vocab), vectors=TEXT.vocab.vectors, 
                                    residual_embeddings=True, model_cache='.embeddings')

  train_iter = data.Iterator(
      (train_dataset),
      batch_size=1, shuffle=False)

  embeddings = {}
  for batch_num, batch in enumerate(train_iter):
    glove_then_last_layer_cove = outputs_cove_with_glove(*batch.concepts)

    v1 = glove_then_last_layer_cove[0].sum(axis=0)
    embeddings[concepts[batch_num+1]] = v1.detach().numpy()

  v1 = embeddings[concept1]
  v2 = embeddings[concept2]
  semantic_relatedness = (1 + (v1.dot(v2)) / (LA.norm(v1) * LA.norm(v2) ) )
  semantic_relatedness /= 2

  return semantic_relatedness