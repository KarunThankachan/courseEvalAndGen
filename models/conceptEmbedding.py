from pytorch_pretrained_bert import BertTokenizer, BertModel
import torch

# Ref : https://pypi.org/project/pytorch-pretrained-bert/
# Bert Tokenizer and Model
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased', do_lower_case=True)
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

# TODO : Ablation study on which BERT embedding works better
def get_bert_embedding(text):
    '''
    '''
    tokens = tokenizer.tokenize(text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokens)
    tokens_tensor = torch.tensor([indexed_tokens])
    encoded_layers, _ = model(tokens_tensor)
    return encoded_layers


# TODO : Ablation study on BERT vs GloVe (look at out of domain samples)
def get_glove_embedding(text):
    '''
    '''
    pass


result = get_bert_embedding("Hello World! How are you today. Wish you well")
print(result[0].shape)
print(len(result))
print(result[0][0])


