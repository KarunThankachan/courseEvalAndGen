import re
import PyPDF2
import sys
import fitz
import csv
import json
from nltk.tokenize import sent_tokenize
from parseTOC import parseTOCContent, extractConceptHierarchyFromTOC
from parseIndex import parseIndexText, extractConceptsFromIndexPage, extractConceptFromIndex

def extractConceptPositionalFeatures(concepts=['and'], path='data', filename="Cloud Computing Bible.pdf", 
                                        pages=(30,495), chapters={1:(10,40), 2:(40,80), 3:(80,102), 4:(102,110)}, 
                                        output="results\\", countOfTocPages=30):
    '''
    Create results\concepts.csv - concept, chapter, pageNumber, lineNumber, wordIdx
    '''
    doc = fitz.open(path+"\\"+filename)
    concept_location = []
    concept_count = len(concepts)
    current_concept = 1

    for concept in concepts:
        concept_location = []
        concept = concept.lower()
        #concept = 'virtualization'
        chapterId = 1
        chapterPageLimit = chapters[chapterId][1]
        
        for pageNumber in range(*pages):
            # get the page number
            while pageNumber > chapterPageLimit+countOfTocPages:
                chapterId += 1
                chapterPageLimit = chapters[chapterId][1]

            page = doc.loadPage(pageNumber)
            text = sent_tokenize(page.getText().lower())
            for i in range(len(text)):
                sent = text[i]
                word_idx = sent.find(concept)
                if concept in text[i]:
                    concept_location.append([concept, str(chapterId), str(pageNumber), str(i), str(word_idx)])

        # write the concepts in this page
        with open("results\concepts2.csv", 'a', newline="") as concept_file:
            wr = csv.writer(concept_file)
            wr.writerows(concept_location)
        
        #empty concept location to save space
        concept_location = []
        print("Concept ", current_concept , " done of total ", concept_count)
        current_concept += 1

    print("Concept Feature Extraction Done")


concepts = extractConceptFromIndex()
print(concepts)
chapters = extractConceptHierarchyFromTOC()
print(chapters)
concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, filename="Cloud Computing Bible.pdf", 
                                         pages=(25,495), chapters=chapters)