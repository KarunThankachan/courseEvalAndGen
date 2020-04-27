from spellchecker import SpellChecker
from nltk import word_tokenize

def is_abbrev_single(a):
    
    a = a.strip()
    
    if a.isupper() and len(word_tokenize(a)) == 0:
        return True
    
    return False

def is_abbrev(a, b):
        
    a_abbrev = ""
    for word in word_tokenize(a.replace("-", " ")):
        a_abbrev += word[0]
        
    if(a_abbrev.strip().lower() == b.strip().lower()):
        return True
    
    b_abbrev = ""
    for word in word_tokenize(b.replace("-", " ")):
        b_abbrev += word[0]
            
    if(b_abbrev.strip().lower() == a.strip().lower()):
        return True
    
    return False

#Returns True if both concepts, a and b refer to the same thing, False otherwise
def entity_resolution(a, b):

    a = a.strip()
    b = b.strip()
    
    #Lowercase
    if a.lower() == b.lower():
        print("Reason: Lowercase")
        return True
    
    a = a.lower()
    b = b.lower()
    
    if is_abbrev(a, b):
        print("Reason: abbrev")
        return True

    #Jumbled
    words_a = [i for i in word_tokenize(a.replace("-", " "))]
    words_b = [i for i in word_tokenize(b.replace("-", " "))]
    if set(words_a) == set(words_b):
        print("Reason: Jumbled/Hyphen")
        return True

    #Spelling mistakes
    spell = SpellChecker()
    misspelled_a = spell.unknown(words_a)
    misspelled_b = spell.unknown(words_b)
    for misspelled_word in misspelled_a:
        words_a[words_a.index(misspelled_word)] = spell.correction(misspelled_word)
        a = a.replace(misspelled_word, spell.correction(misspelled_word))
    for misspelled_word in misspelled_b:
        words_b[words_b.index(misspelled_word)] = spell.correction(misspelled_word)
        b = b.replace(misspelled_word, spell.correction(misspelled_word))

    if set(words_a) == set(words_b):
        print("Reason: Spelling Mistake/Jumbled")
        return True

    #Substring
    if a in b:
        b_rest = b.replace(a, "").replace("(", "").replace(")", "")
        if is_abbrev(a, b_rest):
            print("Reason: abbrev1")
            return True

    if b in a:
        a_rest = a.replace(b, "").replace("(", "").replace(")", "")
        if is_abbrev(b, a_rest):
            print("Reason: abbrev2")
            return True

    return False