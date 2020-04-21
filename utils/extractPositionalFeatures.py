import re
import PyPDF2
import sys
import fitz
import json
from nltk.tokenize import sent_tokenize

def extractConceptPositionalFeatures(concepts=['virtualization'], path='data', filename="Cloud Computing Bible.pdf", 
                                        pages=(25,495), output="results\\"):

    doc = fitz.open(path+"\\"+filename)
    concept_location_dict = {}

    for concept in concepts:
        concept_location = []
        concept = concept.lower()
        #concept = 'virtualization'
        for pageNumber in range(100,110):
            page = doc.loadPage(pageNumber)
            text = sent_tokenize(page.getText().lower())
            for i in range(len(text)):
                if concept in text[i]:
                    concept_location.append([pageNumber, i])
        concept_location_dict[concept] = concept_location
    print(concept_location_dict)
    
    json_dict = json.dumps(concept_location_dict)
    f = open(output + filename+"_concept_locations.json", "w+")
    f.write(json_dict)
    f.close()                
    return concept_location_dict

extractConceptPositionalFeatures()