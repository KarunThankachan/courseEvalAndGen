import csv


def processALCPLdata(path='AL-CPL\\features\\', filename='network_relation_v2.csv'):
    '''
    '''
    with open(path+filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        csv_ouput = []
        for row in csv_reader:
            if int(row[2]) < 0:
                csv_ouput.append([row[1], row[0], '1'])
            elif int(row[2]) > 0:
                csv_ouput.append([row[0], row[1], '1'])
            else:
                csv_ouput.append(row)

    with open(path + "proc_" + filename, 'w', newline="") as concept_file:
        wr = csv.writer(concept_file)
        wr.writerows(['ConceptA','ConceptB','Prereq'])
        wr.writerows(csv_ouput) 

    print("Processed Dataset")

# processALCPLdata(filename='data_mining_relation_v2.csv')
# processALCPLdata(filename='precalculus_relation_v2.csv')
# processALCPLdata(filename='database_relation_v2.csv')
# processALCPLdata(filename='geometry_relation_v2.csv')
# processALCPLdata(filename='macroeconomics_relation_v2.csv')
# processALCPLdata(filename='network_relation_v2.csv')
# processALCPLdata(filename='physics-grade_relation_v2.csv')


def extractConceptsFromGT(path='AL-CPL\\features\\', filename='proc_network_relation_v2.csv'):
    '''
    '''
    print("Extracting concepts from GT")
    concepts = []
    with open(path+filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            concepts.append(row[0].split("(")[0].strip().lower())
            concepts.append(row[1].split("(")[0].strip().lower())
    
    concepts = list(set(concepts))

    # for concept in concepts:
    #     print(concept)

    # print("=="*20)
    return concepts

# print(extractConceptsFromGT())
