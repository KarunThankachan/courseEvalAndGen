import csv
import os

def processALCPLdata(path=os.path.join('AL-CPL','features'), filename='network_relation_v2.csv'):
    '''
    Process data from AL-CPL default format to required format.
    In AL-CPL default format it is concep1, concept2, 0/-1/1
    Required format it is concept1, concept2, 0/1
    '''
    with open(os.path.join(path, filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        csv_ouput = []
        for row in csv_reader:
            # if concept2 is a prequisite of concept 1, flip 
            if int(row[2]) < 0:
                csv_ouput.append([row[1], row[0], '1'])
            # if concpept1 is a prerequite of concept2, keep as is
            elif int(row[2]) > 0:
                csv_ouput.append([row[0], row[1], '1'])
            else:
                csv_ouput.append(row)

    with open(path + "proc_" + filename, 'w', newline="") as concept_file:
        wr = csv.writer(concept_file)
        wr.writerows(['ConceptA','ConceptB','Prereq'])
        wr.writerows(csv_ouput) 

    print("Processed Dataset")

# Code to process all files
# processALCPLdata(filename='data_mining_relation_v2.csv')
# processALCPLdata(filename='precalculus_relation_v2.csv')
# processALCPLdata(filename='database_relation_v2.csv')
# processALCPLdata(filename='geometry_relation_v2.csv')
# processALCPLdata(filename='macroeconomics_relation_v2.csv')
# processALCPLdata(filename='network_relation_v2.csv')
# processALCPLdata(filename='physics-grade_relation_v2.csv')


def extractConceptsFromGT(path=os.path.join('AL-CPL','features'), filename='proc_network_relation_v2.csv'):
    '''
    Get all the concepts present in the groundtruth (AL-CPL) dataset
    '''
    print("Extracting concepts from GT")
    concepts = []
    with open(os.path.join(path, filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            concepts.append(row[0].split("(")[0].strip().lower()) # for multi-word concepts, break on '('
            concepts.append(row[1].split("(")[0].strip().lower())
    
    concepts = list(set(concepts))
    return concepts

# print(extractConceptsFromGT())
