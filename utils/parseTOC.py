import re
import PyPDF2
import sys
import fitz
import json
from nltk.tokenize import sent_tokenize


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parseTOCContent(text, chapterNumber='0'):
    '''
    Creating a dictionary of the concept with page ranges
    '''
    contents = text.splitlines()
    chapter_pages = []
    for content in contents:
        if RepresentsInt(content):
            chapter_pages.append(content)
    return(chapter_pages)


# Entry Point
def extractConceptHierarchyFromTOC(path='data', filename="Cloud Computing Bible.pdf", tocPages=(16,17), \
                                    lastPage=496, output="results\\"):
    '''
    Load textbook, iterate over pages and create concept dictionary
    '''
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    doc = fitz.open(path+"\\"+filename)
    all_chapters = []

    for pageNumber in range(*tocPages):
        page = doc.loadPage(pageNumber)
        text = page.getText()
        chapter_pages = parseTOCContent(text)
        all_chapters += chapter_pages
    
    chapter_dict = {}
    start_value = 0
    chapter_id = 0
    for value in all_chapters:
        end_value = int(value)
        if start_value > end_value:
            print("Parsing Error: ", start_value, end_value)
        chapter_dict[chapter_id] = (start_value, end_value)
        chapter_id += 1
        start_value = int(value)

    chapter_dict[chapter_id] = (start_value, lastPage)
    print(chapter_dict)
    return chapter_dict

# extractConceptHierarchyFromTOC(path='AL-CPL\\textbooks', filename="Networking.pdf", tocPages=(17,25), \
#                                     lastPage=849, output="results\\")

 