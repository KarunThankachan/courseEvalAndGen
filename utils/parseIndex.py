import re
import PyPDF2
import sys
import fitz
import json
from nltk.tokenize import sent_tokenize

def parseIndexText(text):
    '''
    Given Index of the format
    `Cloud Computing ................. 74, 81`
    It will extract as ["Concept Page Numbers", ..]
    '''
    contents = text.splitlines()
    content_with_pns = []
    for i in range(len(contents)-1):
        # check if the next line is numbers only
        if re.search('[a-zA-Z]+', contents[i]) is not None:   
            # if not add to list
            content_with_pns.append(contents[i])
        elif len(content_with_pns) > 1:
            # if yes append to last element for format `Cloud Computing ...... 74, 81 \n 32,22`
            temp = content_with_pns[-1]  
            temp = temp + contents[i]
            content_with_pns[-1] = temp
    return content_with_pns

    

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
            if re.search('[a-zA-Z]+', concept) is not None:
                curr_concepts.append(concept.strip())
            else:
                concept = concept.strip()
                if len(concept) > 0:
                    curr_pages.append(concept.replace("–","-").strip())

        if len(curr_pages) > 0:
            concept_dict.update({curr_concept:curr_pages for curr_concept in curr_concepts})

    # return {concepts:[page numbers, ....]}
    return concept_dict


# Entry Point
def extractConceptFromIndex(path='data', filename="Cloud Computing Bible.pdf", indexPages=(496,528), output="results\\"):
    '''
    To load data from pdf
    Args : filename, name of pdf file
    Rets : the list of concepts from the PDF
    '''
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    doc = fitz.open(path+"\\"+filename)
    all_concepts_dict = {}

    for pageNumber in range(*indexPages):
        page = doc.loadPage(pageNumber)
        text = page.getText()
        content_with_pns = parseIndexText(text)
        all_concepts_dict.update(extractConceptsFromIndexPage(content_with_pns))
    
    json_dict = json.dumps(all_concepts_dict)
    f = open(output + filename+"_concepts.json", "w+")
    f.write(json_dict)
    f.close()
    return all_concepts_dict

all_concepts_dict = extractConceptFromIndex()
print(len(list(all_concepts_dict.keys())))
    