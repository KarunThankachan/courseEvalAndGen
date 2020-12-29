import re
import PyPDF2
import sys
import json
from nltk.tokenize import sent_tokenize
import os
import fitz

def RepresentsInt(s):
    '''
    If argument is an int return true
    else false
    '''
    try: 
        int(s)
        return True
    except ValueError:
        return False


def parseTOCContent(text, toc_type='0'):
    '''
    Creating a dictionary of the concept with page ranges
    Two common type of tocs are handled
    0 - where the page number is on a line alone
    1 - where the chapter title and page number are on the same line
    '''
    contents = text.splitlines()
    chapter_pages = []
    if toc_type == '0':
        for content in contents:
            if RepresentsInt(content): # if an integer
                chapter_pages.append(content) # append to list
    elif toc_type == '1':
        for content in contents:
            page_numbers = re.findall('\d+', content)
            if len(page_numbers) > 0:
                page_number = int(page_numbers[-1])
                if len(chapter_pages) == 0 or chapter_pages[-1] + 100 > page_number:
                    chapter_pages.append(page_number)
    return(chapter_pages)


# Entry Point
def extractConceptHierarchyFromTOC(path, filename, tocPages, tocType, lastPage, output="results\\"):
    '''
    Load textbook, iterate over pages and create concept dictionary
    '''
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    # f = open(os.path.join(path, filename), "rb")
    # doc = PyPDF2.PdfFileReader(f) 
    doc = fitz.open(os.path.join(path, filename))
    
    all_chapters = []

    for pageNumber in range(*tocPages):
        text = doc.loadPage(pageNumber).getText()
        chapter_pages = parseTOCContent(text, tocType) # extract page number from each line
        all_chapters += chapter_pages
    
    chapter_dict = {}
    start_value = 0
    chapter_id = 0
    for value in all_chapters:
        end_value = int(value)
        if start_value > end_value:
            print("Parsing Error: ", start_value, end_value) # to avoid out-of-order chapter ranges
            continue
        chapter_dict[chapter_id] = (start_value, end_value)
        chapter_id += 1
        start_value = int(value)

    chapter_dict[chapter_id] = (start_value, lastPage)
    print(chapter_dict)
    return chapter_dict


# extractConceptHierarchyFromTOC(path=os.path.join('AL-CPL','textbooks'), filename="Networking.pdf", tocPages=(17,25), \
#                                     tocType='1', lastPage=849, output="results\\")

 