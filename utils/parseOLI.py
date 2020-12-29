import os
import csv
from nltk.tokenize import sent_tokenize

def extractConceptsFromOLI(data_path='OLIData', filename='concepts'):
    '''
    '''
    concepts = []
    with open(os.path.join(data_path, filename)) as f:
        for line in f.readlines():
            concepts.append(line.strip().lower())
    return concepts


def extractOLIIndex(data_path='OLIData', data_dir='data'):
    '''
    250-300 words per page
    Unit + Module => Chapter
    Divide content in a chapter into pages
    '''
    units = os.listdir(os.path.join(data_path, data_dir))
    chap_no = 1
    page_no = 1
    data_dict = {}
    for unit in units:
        modules = os.listdir(os.path.join(data_path, data_dir, unit))
        for module in modules:
            chapters = os.listdir(os.path.join(data_path, data_dir, unit, module))
            for chapter in chapters:
                with open(os.path.join(data_path, data_dir, unit, module, chapter), encoding='utf-8') as f:
                    page_data = ""
                    for line in f.readlines():
                        page_data = page_data + " " + line.strip()
                        if len(page_data.split()) > 300:
                            page_no += 1
                            data_dict[(chap_no, page_no)] = page_data
                            page_data = ""
                        
                chap_no += 1
    return data_dict

def extractPositionalFeaturesforOLI(concepts, data_dict, output="results\\"):
    concept_location = []
    count_concepts = len(concepts)
    curr_count = 1
    for concept in concepts:
        for key,value in data_dict.items():
                text = sent_tokenize(value)
                for i in range(len(text)):
                    sent = text[i]
                    word_idx = sent.find(concept) 
                    if concept in text[i]:
                        concept_location.append([concept, str(key[0]), str(key[1]), str(i), str(word_idx)])
        
        print("Concept ", curr_count, " completed of total ", count_concepts)
        curr_count += 1
    out_file = "olidata.csv"
    with open(output + out_file, 'w', newline="") as concept_file:
        wr = csv.writer(concept_file)
        wr.writerows(concept_location)
    print("Concept Feature Extraction Done")

concepts = extractConceptsFromOLI()
data_dict = extractOLIIndex()
extractPositionalFeaturesforOLI(concepts, data_dict)            
