import re
import PyPDF2
import sys
import fitz
import json
from nltk.tokenize import sent_tokenize

def parseTOCContent(text, chapterNumber='0'):
    '''
    Creting a dictionary of the concept with page ranges
    '''
    contents = text.splitlines()
    contents = [content.split(',') for content in contents]
    chapter_dict = {}
    for content in contents:
        newChapterNames = re.findall('[a-zA-z\s\(\)]+', content[0])
        newChapterPageNumber = re.findall('[0-9]+$', content[0])
        if len(newChapterNames) > 1 :
            newChapterName = newChapterNames[1]
        elif len(newChapterNames) > 0:
            newChapterName = newChapterNames[0]
        if len(newChapterPageNumber) > 0:
            chapter_dict[newChapterName.strip()] = int(newChapterPageNumber[0])
    return(chapter_dict)


# Entry Point
def extractConceptHierarchyFromTOC(path='data', filename="Cloud Computing Bible.pdf", tocPages=(16,17), \
                                    lastPage=496, output="results\\"):
    '''
    Load textbook, iterate over pages and create concept dictionary
    '''
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    doc = fitz.open(path+"\\"+filename)
    all_concepts_dict = {}

    for pageNumber in range(*tocPages):
        page = doc.loadPage(pageNumber)
        text = page.getText()
        chapter_dict = parseTOCContent(text)
        all_concepts_dict.update(chapter_dict)
    
    chapter_dict = {}
    start_value = 0
    chapter_id = 0
    for key, value in all_concepts_dict.items():
        end_value = value
        chapter_dict[chapter_id] = (start_value, end_value, key)
        chapter_id += 1
        start_value = value

    chapter_dict[chapter_id] = (start_value, lastPage)
    return chapter_dict

extractConceptHierarchyFromTOC()

 