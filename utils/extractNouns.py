import nltk
import spacy

nlp = spacy.load("en_core_web_sm")

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


def extractNounsSapcy(text):
    '''
    '''
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)
    return(chunk.text)