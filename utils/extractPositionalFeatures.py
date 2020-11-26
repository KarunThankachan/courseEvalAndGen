import re
import PyPDF2
import sys
import fitz
import csv
import json
from nltk.tokenize import sent_tokenize
from parseTOC import parseTOCContent, extractConceptHierarchyFromTOC
from parseIndex import parseIndexText, extractConceptsFromIndexPage, extractConceptFromIndex
from parseALCPL import extractConceptsFromGT

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

    # write the concepts in this page
    out_file = filename.split(".")[0] + "_concepts.csv"

    # clear file content
    f = open(output + out_file , 'w+')
    f.truncate(0) # need '0' when using r+
    f.close()
        

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

        with open(output + out_file, 'a', newline="") as concept_file:
            wr = csv.writer(concept_file)
            wr.writerows(concept_location)
        
        #empty concept location to save space
        concept_location = []
        print("Concept ", current_concept , " done of total ", concept_count)
        current_concept += 1

    print("Concept Feature Extraction Done")


filename = 'Networking.pdf'
path = "AL-CPL\\textbooks\\"
gt_filename = "proc_network_relation_v2.csv"
concepts = extractConceptFromIndex(path, filename, indexPages=(849,889))
concepts = extractConceptsFromGT(path, gt_filename)
chapters = extractConceptHierarchyFromTOC(path, filename, tocPages=(17,25), lastPage=849, output="results\\")
concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=path, filename=filename, pages=(27,849), chapters=chapters)


txt_path = "AL-CPL\\textbooks\\"
feature_path = "AL-CPL\\features\\"

# filename = 'DBMS.pdf'
# gt_filename = "proc_database_relation_v2.csv"
# concepts = extractConceptFromIndex(txt_path, filename, indexPages=(1084,1096))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(9,26), lastPage=1083, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(37,1083), chapters=chapters)

# filename = 'Precalculus.pdf'
# gt_filename = "proc_precalculus_relation_v2.csv"
# concepts = extractConceptFromIndex(txt_path, filename, indexPages=(999, 1010))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(10,15), lastPage=998, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(33,998), chapters=chapters)

# # TOC is different
# filename = 'Economics.pdf'
# gt_filename = "proc_macroeconomics_relation_v2.csv"
# concepts = extractConceptFromIndex(txt_path, filename, indexPages=(852,859))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(22,36), lastPage=852, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(39,852), chapters=chapters)

# filename = 'Physics.pdf'
# gt_filename = "proc_physics-grade_relation_v2.csv"
# # concepts = extractConceptFromIndex(path, filename, indexPages=(849,889))
# concepts = extractConceptsFromGT(feature_path, gt_filename)
# chapters = extractConceptHierarchyFromTOC(txt_path, filename, tocPages=(4,18), lastPage=700, output="results\\")
# concept_location_dict = extractConceptPositionalFeatures(concepts = concepts, path=txt_path, filename=filename, pages=(20,700), chapters=chapters)
