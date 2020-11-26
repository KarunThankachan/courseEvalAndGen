import csv
import json

def getAdditionalConceptDetails(concept_features):
    '''
    '''
    concept_chapters = {}
    concept_locations = {}
    for concept in concept_features:
        if concept[0] in concept_chapters:
            concept_chapters[concept[0]] += [concept[1]]
            concept_locations[concept[0]] += [[concept[1], concept[2], concept[3], concept[4]] ]
        else:
            concept_chapters[concept[0]] = [concept[1]]
            concept_locations[concept[0]] = [[concept[1], concept[2], concept[3], concept[4]]]
    
    # chapter density score
    concept_chapter_density = {}
    for concept, chapters in concept_chapters.items():
        concept_chapter_density[concept] = len(set(chapters))
    
    return concept_chapter_density, concept_locations

def getDADSCore(conceptA_locs, conceptB_locs):

    # hyper parameter
    sent_imp = 0.5
    word_imp = 0.1

    all_dad = 0
    for conceptA_loc in conceptA_locs:
        page_dad = 10000
        sent_dad = 10000
        word_dad = 10000
        for conceptB_loc in conceptB_locs:
            if conceptA_loc[0] == conceptB_loc[0]:
                page_dist = int(conceptA_loc[1]) - int(conceptB_loc[1]) 
                sent_dist = int(conceptA_loc[2]) - int(conceptB_loc[2])
                word_dist = int(conceptA_loc[3]) - int(conceptB_loc[3])
                if abs(page_dist) < abs(page_dad):
                    page_dad = page_dist
                if page_dist == 0 and abs(sent_dist) < abs(sent_dad):
                    sent_dad = sent_dist
                if sent_dist == 0 and abs(word_dist) < abs(word_dad):
                    word_dad = word_dist
        all_dad += page_dad + sent_dad * sent_imp + word_dad * word_imp
    if all_dad > 1000:
        return 1000
    elif all_dad < -1000:
        return -1000
    else:
        return all_dad


def createAdditionalFeatures(path="results\\", filename='Networking_concepts.csv'):
    '''
    '''
    concept_features = []
    with open(path+filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            concept_features.append(row)

    concept_chapter_density, concept_locations = getAdditionalConceptDetails(concept_features)
    concepts = list(concept_locations.keys())
    print("Total Number of concepts: ", len(concepts))

    concept_features = {}
    concept_count = 1
    for concept_A in concepts:
        for concept_B in concepts:
            if concept_A != concept_B:
                dad_score = getDADSCore(concept_locations[concept_A], concept_locations[concept_B])
                concept_chapter_density_A = concept_chapter_density[concept_A]
                concept_chapter_density_B = concept_chapter_density[concept_B]
                complexity = ( concept_chapter_density_A + concept_chapter_density_B ) /  ( concept_chapter_density_A * concept_chapter_density_B )
                concept_features[concept_A, concept_B] = [complexity , dad_score ]
        print("Concept", concept_count, "done")
        concept_count += 1

    filename_stub = filename.split('.')[0]
    with open(filename_stub+"_additional", 'w') as outfile:
        for key, value in concept_features.items():
            out_str = key[0] + "," + key[1] + "," + str(value[0]) + "," + str(value[1]) + "\n"
            outfile.write(out_str)
                    

createAdditionalFeatures(path="results\\", filename='Networking_concepts.csv')

