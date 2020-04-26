import csv
import sys
sys.path.append("utils")
from parseIndex import parseIndexText, extractConceptsFromIndexPage, extractConceptFromIndex


def extractConceptsFromGT(path='AL-CPL\\features\\', filename='proc_network_relation_v2.csv'):
    '''
    '''
    print("Extracting concepts from GT")
    concepts = []
    with open(path+filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            concepts.append(row[0].lower())
            concepts.append(row[1].lower())
    
    concepts = list(set(concepts))

    # for concept in concepts:
    #     print(concept)

    # print("=="*20)
    return concepts



def evaluateConceptExtraction(path="", filename=""):
    '''
    '''
    concepts =  extractConceptFromIndex(path="AL-CPL\\textbooks\\", filename='Networking.pdf')
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



