# Create pre-requisite graph as an inverted list
import os

concept_prereqs = {}
with open(os.path.join("OLIData","results","OLIData.csv")) as f:
    next(f)
    for line in f.readlines():
        conceptA, conceptB, label = line.split(',')
        label = int(label.strip())
        if label == 1:
            if conceptB not in concept_prereqs: 
                concept_prereqs[conceptB] = [conceptA]
            else:
                concept_prereqs[conceptB].append(conceptA)



tests = ['hyperparameters', 'supervised learning', 'cross-validation']
for test in tests:
    print("Seeding with : ", test)
    prereqs = []
    concept_pairs = []
    i = 0
    prereqs.append(test)
    while i < len(prereqs):
        prereq = prereqs[i]
        if prereq in concept_prereqs:
            for concept in concept_prereqs[prereq]:
                if concept not in prereqs:
                    concept_pairs.append([concept, prereq, 1])
        i = i + 1
    print(concept_pairs)







