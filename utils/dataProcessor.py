import nltk

def extractNouns(text):
    ''' 
    Tokenization, POS Tagging and Extraction of noun pharase
    Args : text, a string
    Ret : list of nouns in string
    '''
    
    concepts = []
    text = nltk.sent_tokenize(text)
    for sentence in text:
     for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
             concepts.append(word)
    #print(text, concepts)
    return concepts


def extractConcepts(text):
    '''
    '''
    pass