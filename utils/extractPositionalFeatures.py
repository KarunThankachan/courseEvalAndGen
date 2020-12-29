import re
import PyPDF2
import sys
import csv
import json
import os
from nltk.tokenize import sent_tokenize
from parseTOC import parseTOCContent, extractConceptHierarchyFromTOC
from parseIndex import parseIndexText, extractConceptsFromIndexPage, extractConceptFromIndex
from parseALCPL import extractConceptsFromGT

def extractConceptPositionalFeatures(concepts, path, filename, pages, chapters, output="results\\" ):
    '''
    Create results\concepts.csv - concept, chapter, pageNumber, lineNumber, wordIdx
    '''
    countOfTocPages = pages[0]+1
    f = open(os.path.join(path, filename), "rb")
    doc = PyPDF2.PdfFileReader(f) 
    concept_location = []
    concept_count = len(concepts)
    current_concept = 1

    # write the concepts in this page
    out_file = filename.split(".")[0] + "_concepts.csv"

    # clear file content
    f = open(output + out_file , 'w+')
    f.truncate(0) # need '0' when using w+
    f.close()
        
    for concept in concepts:
        concept_location = []
        concept = concept.lower()
        # test example
        # concept = 'virtualization'
        # get the first chapter and chapter last page
        chapterId = 1
        chapterPageLimit = chapters[chapterId][1]
        for pageNumber in range(*pages):
            # get the page number for the next chapter
            while pageNumber > chapterPageLimit+countOfTocPages:
                chapterId += 1
                chapterPageLimit = chapters[chapterId][1]
            # load text in the page
            text = sent_tokenize(doc.getPage(pageNumber).extractText().lower()) # process
            for i in range(len(text)): # for each sentence
                sent = text[i]
                word_idx = sent.find(concept)  # find idx of concept in sent (-1 if not present)
                if concept in text[i]: # check if concept in sent
                    # add concept_name, chapter_id, page_no, sentence_no, word_no
                    concept_location.append([concept, str(chapterId), str(pageNumber), str(i), str(word_idx)])
        # write concept details to output file
        with open(output + out_file, 'a', newline="") as concept_file:
            wr = csv.writer(concept_file)
            wr.writerows(concept_location)
        # empty concept location - space utilization
        concept_location = []
        print("Concept ", current_concept , " done of total ", concept_count)
        current_concept += 1

    print("Concept Feature Extraction Done")


# txt_path = os.path.join("OLIData")
# filename = 'Cloud_Computing_Bible.pdf'
# concepts = extractConceptFromIndex(txt_path, filename , indexPages=(495,527))
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(18,23), tocType='1', lastPage=494, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(18,494), chapters=chapters)

txt_path = os.path.join("OLIData")
filename = 'Foundations of Data Science - Cornell CS.pdf'
concepts = extractConceptFromIndex(txt_path, filename , indexPages=(465,469))
print(concepts)
chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(1,8), tocType='1', lastPage=465, output="results\\")
concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(9,465), chapters=chapters)

txt_path = os.path.join("OLIData")
filename = 'pythondatasciencehandbook.pdf'
concepts = extractConceptFromIndex(txt_path, filename , indexPages=(534,548))
chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(5,12), tocType='1', lastPage=534, output="results\\")
concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(13,533), chapters=chapters)

# txt_path = os.path.join("AL-CPL","textbooks")
# feature_path = os.path.join("AL-CPL","features")

# filename = 'Networking.pdf'
# gt_filename = "proc_network_relation_v2.csv"
# # concepts = extractConceptFromIndex(txt_path, filename, indexPages=(849,889)) # TODO :  replace with concept extraction
# concepts = extractConceptsFromGT(feature_path, gt_filename) # TODO : replace with concept extraction
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(17,25), tocType='1', lastPage=849, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(27,849), chapters=chapters)

# filename = 'DBMS.pdf'
# gt_filename = "proc_database_relation_v2.csv"
## concepts = extractConceptFromIndex(txt_path, filename, indexPages=(1084,1096))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(9,26), lastPage=1083, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(37,1083), chapters=chapters)

# filename = 'Precalculus.pdf'
# gt_filename = "proc_precalculus_relation_v2.csv"
## concepts = extractConceptFromIndex(txt_path, filename, indexPages=(999, 1010))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(10,15), lastPage=998, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(33,998), chapters=chapters)

# filename = 'Economics.pdf'
# gt_filename = "proc_macroeconomics_relation_v2.csv"
## concepts = extractConceptFromIndex(txt_path, filename, indexPages=(852,859))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(22,36), lastPage=852, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(39,852), chapters=chapters)

# filename = 'Physics.pdf'
# gt_filename = "proc_physics-grade_relation_v2.csv"
## concepts = extractConceptFromIndex(path, filename, indexPages=(849,889))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(4,18), lastPage=700, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(20,700), chapters=chapters)
