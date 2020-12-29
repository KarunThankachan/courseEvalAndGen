import re
import PyPDF2
import sys
import json
from nltk.tokenize import sent_tokenize
import os


def extractConceptsFromIndexPage(content_with_pns):
    '''
    Extract concepts given the index page of a text book
    '''
    concept_dict = {}

    for content in content_with_pns:
        concepts = content.split(',')
        curr_concepts = []
        curr_pages = []
        for concept in concepts:
            # name of the concepts
            if re.search('[a-zA-Z]+', concept) is not None:
                curr_concepts.append(concept.strip())
            else:
            # page number of concept
                concept = concept.strip()
                if len(concept) > 0:
                    curr_pages.append(concept.replace("–","-").strip())

        if len(curr_pages) > 0:
            concept_dict.update({curr_concept:curr_pages for curr_concept in curr_concepts})

    return concept_dict


def parseIndexText(text):
    '''
    Given Index of the format
    `Cloud Computing ................. 74, 81`
    It will extract as ["Concept Page Numbers", ..]
    '''
    contents = text.splitlines()
    content_with_pns = []
    for i in range(len(contents)):
        # if the next line is contains no numbers, then it a continuation of the concept
        # append it to last element in the concept list
        if (len(content_with_pns) > 1) and (re.search('[0-9]+',content_with_pns[-1]) is None):
            content_with_pns[-1] =  content_with_pns[-1] + " " + contents[i]
        # else if next line contains letters and numbers, then create a new element in the list
        elif re.search('[a-zA-Z]+', contents[i]) is not None:   
            content_with_pns.append(contents[i])
        # if there are only number left, add to last entry
        elif len(content_with_pns) > 1:
            content_with_pns[-1] = content_with_pns[-1] + contents[i]
    return content_with_pns


# Entry Point
def extractConceptFromIndex(path, filename, indexPages, output="results\\"):
    '''
    To load data from pdf
    Args : filename, name of pdf file
    Rets : the list of concepts from the PDF
    '''
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    f = open(os.path.join(path,filename), "rb")
    doc = PyPDF2.PdfFileReader(f) 
    all_concepts_dict = {}

    for pageNumber in range(*indexPages):
        text = doc.getPage(pageNumber).extractText()
        content_with_pns = parseIndexText(text)
        all_concepts_dict.update(extractConceptsFromIndexPage(content_with_pns))
    
    json_dict = json.dumps(all_concepts_dict)
    f = open(output + filename+"_concepts.json", "w+")
    f.write(json_dict)
    f.close()


    # return {concepts:[page numbers, ....]}
    concept_names_raw = list(all_concepts_dict.keys())
    concept_names = []
    for concept_name in concept_names_raw:
        if (concept_name not in concept_names) and (concept_name+"s" 
                    not in concept_names) and (concept_name[:-1] not in concept_names):
            concept_names.append(concept_name)

    return concept_names


# test script
# concepts = extractConceptFromIndex(path=os.path.join("AL-CPL","textbooks"), filename='Networking.pdf', indexPages=(849,889))

# print(concepts)
# print(len(concepts))
    