import PyPDF2
import sys

sys.path.append('utils')
from dataProcessor import extractNouns

def extract_concepts(path='data', filename="Hand Book of Cloud Computing.pdf"):
    '''
    To load data from pdf
    Args : filename, name of pdf file
    Rets : the list of concepts from the PDF
    '''
    
    # TODO : Path should be passed as argument
    # Ref : https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
    file = open(filename, "rb",)
    pdf_file = PyPDF2.PdfFileReader(file)
    all_concepts = []

    #for page in range(pdf_file.numPages):
    for page in range(5):
        page_obj = pdf_file.getPage(page)
        text = page_obj.extractText()
        all_concepts += extractNouns(text)

    file.close()
    return all_concepts

concepts = extract_concepts()
print(concepts)