__author__ = 'abhisheksharma'

################################################## EXTRACT_OBJECTS #####################################################
# Function Defination 1: Extract_Objects

def extract_objects(data):

    two_nouns=[]
    secondNN =[]
    firstNN = []
    nouns=[]
    i=0
    additional_stop_list=["employee", "employees" "water","injure","power", "wall","blasting","struck", "worker","farm", "way", "exposure", "ice", "removal", "roofer", "ft","concussion", "safety","guy","slip", "renovation","fallen","hurt", "eye" "sand","caught" , "wet", "catwalk", "driver", "collapse","construction","fall","injury", "floor", "system", "excavation", "space", "work", "elevation", "roof", "utlilty", "structure", "light",  "counterweight", "extension", "communication", "flying", "installation","establishment", "explosion","unkown","return", "load", "air","ppe", "consciousness", "incident", "accident", "burn", "head", "collapse", "object", "foot", "leg", "boom", "space", "arm", "line", "ankle", "hip", "light", "demolition", "ground", "carpenter", "home", "work", "fracture", "exhaustion", "pool", "operation", "block", "face", "k", "auger", "work-zone", "edge", "amputation", "circular", "wrist", "structure", "system", ""]
    final_object=[]

    for parag in data:
        i = i + 1
        print "------------------------------- Text: ", i ," -------------------------------"
        print parag
        print '\n'
        text=str(parag).encode('ascii','ignore')
        text=text.translate(string.maketrans("",""), string.punctuation)
        text=text.lower()
        stop = stopwords.words('english')
        stop.extend(additional_stop_list)

        text_nostop=" ".join(filter(lambda word: word not in stop, text.split()))

        token=nltk.word_tokenize(text_nostop)

        posTag=nltk.pos_tag(token)

        nouns= [word for word,pos in posTag if (pos == 'NN')]

        try:

            if not nouns:
                nouns=["no_object"]


            firstNN = nouns[-2]
            secondNN = nouns[-1]
            two_nouns.append(firstNN)
            two_nouns.append(secondNN)
            noun_ph=firstNN +" "+ secondNN

            data1=parag.lower()
            #print "Processing Line ",i,"= Lowered Data =",data1

            if (noun_ph in data1):

                print "2a). -----Two Nouns Matched: -----)"

                noun_ph = noun_ph.replace(" ", "-")

                final_object.append(noun_ph)
            else:
                final_object.append(nouns[-1])
            #print '\n'

        except Exception, e:
            final_object.append(nouns[-1])
            continue

    j=0
    print "This is the list of objects: "
    print final_object
    #print '\n'
    for i in final_object:

        if i=='shock':
            final_object[j]='power-line'
        j=j+1
    return final_object

######################################################### COUNTS #######################################################
# Function Defination 2: Counts

def counts(final_object):
    counts = collections.Counter(final_object)
    #print "Total Count for each Objects: ", counts
    return counts

####################################################### WORD CLOUD #####################################################
# Function Defination 3: Word Cloud

def word_cloud(final_object, cloud_object):

    import re
    from pytagcloud.lang.stopwords import StopWords
    from operator import itemgetter
    final_object = [x for x in final_object if x != "no_object"]


    counted = {}

    for word in final_object:
        if len(word) > 1:
            if counted.has_key(word):
                counted[word] += 1
            else:
                counted[word] = 1
    #print len(counted)

    counts = sorted(counted.iteritems(), key=itemgetter(1), reverse=True)

    print "Total count of Word Cloud List Items: ",counts
    #type(counts)

    words = make_tags(counts, maxsize=100)
    print "Word Cloud List items: ", words


    create_tag_image(words, 'cloud_1_All_Objects.png', size=(1280, 900), fontname='Lobster')

    width = 1280
    height = 800
    layout = 3
    background_color = (255, 255, 255)
    #create_tag_image(words, 'cloud_2_All_Objects.png', size=(width, height), layout=layout, fontname='Crimson Text', background = background_color)



####################################################### MAIN FUNCTION ##################################################

import nltk
import pandas as pd
import collections
import string
import re
from nltk.corpus import stopwords
from pytagcloud import create_tag_image, make_tags, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud.lang.stopwords import StopWords
from operator import itemgetter
global collections
global operator
global create_tag_image
global make_tags
global LAYOUTS
global get_tag_counts

def main():

    # Read Data
    file= pd.read_excel('/Users/abhisheksharma/Documents/Study/Text Mining/CA_Text_Mining_Folder_SLFiles/CA_TM_Data_Code/filtered_construction_data_refined.xlsx')
    df = file.ix[0:,0:3]
    data=file.ix[0:,1]

    # Extract Objects:
    final_object_cloud = extract_objects(data)

    # Count each word occurence:
    counts(final_object_cloud)

     # Word Clouds:
    word_cloud(final_object_cloud, "My_word_Cloud")

    # Save output file:
    df['Objects2']=pd.DataFrame(final_object_cloud)
    writer = pd.ExcelWriter("/Users/abhisheksharma/Documents/Study/Text Mining/CA_Text_Mining_Folder_SLFiles/CA_TM_Data_Code/objects.xlsx")
    df.to_excel(writer)
    writer.save()

if __name__ == '__main__':main()


####################################################### END ############################################################
