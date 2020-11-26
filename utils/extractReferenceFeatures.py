import csv
import json

def createComplexityFeature(concept_features):
    '''
    '''
    concept_complexity = {}
    concept_chapters = {}
    concept_locations = {}
    for concept in concept_features:
        if concept[0] in concept_complexity:
            concept_complexity[concept[0]] += 1
        else:
            concept_complexity[concept[0]] = 1
    
    return concept_complexity


def createReferenceFeatures(path="results\\", filename='Networking_concepts.csv'):
    '''
    '''
    concept_features = []
    with open(path+filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            concept_features.append(row)

    concept_complexity = createComplexityFeature(concept_features)
    #print(concept_complexity)

    chapterIdx = 0
    pageIdx = 0
    sentenceIdx = 0
    wordIdx = 0
    complexityIdx = 0

    conceptA = concept_features
    conceptB = concept_features

    concept_refs = {}
    concept_count = len(conceptA)
    curr_concept_count = 0
    for c_A in conceptA:
        c_A_concept, c_A_chapter, c_A_page, c_A_sentence, c_A_word = c_A
        c_A_complexity = concept_complexity[c_A_concept]
        for c_B in conceptB:
            c_B_concept, c_B_chapter, c_B_page, c_B_sentence, c_B_word = c_B
            c_B_complexity = concept_complexity[c_B_concept]
            # check concepts are different
            if c_B_concept != c_A_concept:
                # calculate complexity distance
                ref_complexity_dist = c_A_complexity - c_B_complexity
                ref_line_dist, ref_word_dist, ref_line_flag , ref_word_flag = None, None,  0 , 0
                # chapter distnace
                ref_chap_dist = int(c_A_chapter) - int(c_B_chapter)
                # page distance
                ref_page_dist = int(c_A_page) - int(c_B_page)
                # line distance
                if ref_page_dist == 0:
                    ref_line_dist = int(c_A_sentence) - int(c_B_sentence)
                    ref_line_flag = 1
                # word distance
                if ref_line_dist == 0:
                    ref_word_dist = int(c_A_word) - int(c_B_word)
                    ref_word_flag = 1
                else:
                    ref_line_dist = 0
                    ref_word_dist = 0


                if (c_A_concept, c_B_concept) not in concept_refs:
                    concept_refs[(c_A_concept, c_B_concept)] = [ref_chap_dist, 
                        ref_page_dist, ref_line_dist, ref_word_dist, 1, ref_line_flag, ref_word_flag, ref_complexity_dist, 0, 0]
                else:
                    concept_refs[(c_A_concept, c_B_concept)][0] += ref_chap_dist
                    concept_refs[(c_A_concept, c_B_concept)][1] += ref_page_dist
                    concept_refs[(c_A_concept, c_B_concept)][2] += ref_line_dist
                    concept_refs[(c_A_concept, c_B_concept)][3] += ref_word_dist
                    concept_refs[(c_A_concept, c_B_concept)][4] += 1
                    concept_refs[(c_A_concept, c_B_concept)][5] += ref_line_flag
                    concept_refs[(c_A_concept, c_B_concept)][6] += ref_word_flag

        curr_concept_count += 1
        print("Concept ", curr_concept_count, " completed of total ", concept_count)

    filename = filename.split(".")[0] + "_features.csv"

    # clear file content
    f = open(path + filename , 'w')
    f.truncate(0) # need '0' when using r+
    f.close()
        
    with open(path+filename, 'a', newline="", encoding="utf-8") as concept_file:
        for key,value in concept_refs.items():
            out_val = key[0] + "," + key[1] + "," + str(value[0]) + "," + str(value[1]) + "," + \
                str(value[2]) + "," + str(value[3]) + "," + str(value[4]) + "," + \
                    str(value[5]) + "," + str(value[6]) + "," + str(value[7]) + "\n"
            concept_file.write(out_val)
    
    return

#createReferenceFeatures(path="results\\", filename='Networking_concepts.csv')
createReferenceFeatures(path="results\\", filename='Economics_concepts.csv')
createReferenceFeatures(path="results\\", filename='Physics_concepts.csv')
            