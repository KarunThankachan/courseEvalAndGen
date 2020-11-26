import csv
import sys
sys.path.append("utils")
from parseIndex import parseIndexText, extractConceptsFromIndexPage, extractConceptFromIndex






def evaluateConceptExtraction(path="AL-CPL\\textbooks\\", filename='Networking.pdf'):
    '''
    '''
    filename = filename.split('.')[0]
    concepts =  extractConceptFromIndex(path, filename)
    concepts = [concept.lower() for concept in concepts]

    f = open("networking_found","w", encoding="utf-8")
    for concept in concepts:
        f.write(concept+"\n")
    f.close()

    gt_concepts = extractConceptsFromGT()

    nt_found = open("error_analysis\\conceptExtraction\\networking_found", "w", encoding="utf-8")
    for concept in concepts:
        nt_found.write(concept+"\n")
    nt_found.close()

    nt_missed = open("error_analysis\\conceptExtraction\\networking_missed", "w", encoding="utf-8")
    count = 0
    for gt_concept in gt_concepts:
        for concept in concepts:
            if gt_concept in concept:
                count += 1
                break
        else:
            nt_missed.write(gt_concept+"\n")
            
    nt_missed.close()
    gt_count = len(gt_concepts)
    print("Found ", count, " of total ", gt_count)

evaluateConceptExtraction()



