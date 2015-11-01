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

def word_cloud(final_object, file_path, max_words, width, height):
    stop = util.stopwords
    # temp_obj = [x for x in final_object if x != "no_object"]
    temp_obj = final_object.most_common(max_words)

    max_count = max(temp_obj, key=operator.itemgetter(1))[1]
    temp_obj = [(name, count / float(max_count))for name, count in temp_obj]
    temp_obj.pop(0) # remove "no_object"

    word_cloud = WordCloud(font_path="fonts/Georgia.ttf",
        width=width, height=height, max_words=max_words, stopwords=stop)
    word_cloud.fit_words(temp_obj)
    word_cloud.to_file(file_path + ".png")


####################################################### MAIN FUNCTION ##################################################

from lib.util import *

util = Util()
def main():
    # Read Data
    file = pd.read_csv('result/1_osha_filter_scrapper.csv')
    df = file.ix[0:,0:3]
    data=file.ix[0:,1]

    # Extract Objects:
    final_object_cloud = extract_objects(data)

    # Count each word occurence:
    count_object = counts(final_object_cloud)

     # Word Clouds:
    word_cloud(count_object, "result/3_question2", 50, 1280, 800)

    # Save output file:
    df['Objects2'] = pd.DataFrame(final_object_cloud)
    df.to_csv('result/3_question2.csv', index = False)
    print("========DONE==========")

if __name__ == '__main__':main()


####################################################### END ############################################################
