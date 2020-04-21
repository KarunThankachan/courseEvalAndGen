import re
import PyPDF2
import sys
import fitz
import json
from nltk.tokenize import sent_tokenize

def parseTOCContent(text, chapterNumber='0'):
    '''
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


def extractConceptHierarchyFromTOC(path='data', filename="Cloud Computing Bible.pdf", tocPages=(18,27), output="results\\"):
    '''
    '''
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    doc = fitz.open(path+"\\"+filename)
    all_concepts_dict = {}

    for pageNumber in range(*tocPages):
        page = doc.loadPage(pageNumber)
        text = page.getText()
        chapter_dict = parseTOCContent(text)
        all_concepts_dict.update(chapter_dict)
    json_dict = json.dumps(all_concepts_dict)
    f = open(output + filename+"_TOC.json", "w+")
    f.write(json_dict)
    f.close()

    return all_concepts_dict

 
#extractConceptHierarchyFromTOC()