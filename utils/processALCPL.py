import csv


def processALCPLdata(path='AL-CPL\\features\\', filename='network_relation_v2.csv'):
    '''
    '''
    with open(path+filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        csv_ouput = []
        for row in csv_reader:
            if int(row[2]) == -1:
                csv_ouput.append([row[1], row[0], '1'])
            else:
                csv_ouput.append(row)

    with open(path + "proc_" + filename, 'w', newline="") as concept_file:
        wr = csv.writer(concept_file)
        wr.writerows(csv_ouput) 

    print("Processed Dataset")

# processALCPLdata(filename='data_mining_relation_v2.csv')
# processALCPLdata(filename='precalculus_relation_v2.csv')
# processALCPLdata(filename='database_relation_v2.csv')
# processALCPLdata(filename='geometry_relation_v2.csv')
# processALCPLdata(filename='macroeconomics_relation_v2.csv')
# processALCPLdata(filename='network_relation_v2.csv')
# processALCPLdata(filename='physics-grade_relation_v2.csv')
