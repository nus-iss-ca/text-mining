from lib.util import *
import re

util = Util()

#load data
osha_data = pd.read_csv("result/1_osha_filter_scrapper.csv")
osha_data.columns = ['id', 'title', 'summary']

temp_summary = []
for index, row in osha_data.iterrows():
    m = re.findall(r'was ([^.]*).', row["summary"])
    n = re.findall(r'were ([^.]*).', row["summary"])
    temp_summary.append(m + n)

pos_array = []
for row in temp_summary:
    temp_array = []
    for summary in row:
        temp_pos = pos_tag(wt(summary))
        for i in range(0, len(temp_pos)):
            temp_sentence = ""
            temp_index = 0
            if temp_pos[i][1] == "VBG": # only get V-ing
                for j in range(i, len(temp_pos)):
                    temp_sentence = temp_sentence + " " + temp_pos[j][0]
                    temp_index = temp_index + 1
                    if temp_index == 4:
                        break
            if not temp_sentence == "":
                temp_array.append(temp_sentence.rstrip())
    pos_array.append(temp_array)

final_text = []
counter_array = []
for row in pos_array:
    temp_array = []
    for sentence in row:
        temp_text = util.normalize(sentence)
        temp_text = util.remove_punctuation(sentence, "", "")
        temp_text = temp_text.lower()
        temp_tokens = wt(temp_text)
        temp_text = util.lemmatize(temp_tokens)
        temp_array.append(temp_text)
        counter_array.append(temp_text)
    final_text.append(temp_array)

# export to world cloud
counts = collections.Counter(counter_array)
counts += collections.Counter()
final = counts.most_common(50)
max_count = max(final, key=operator.itemgetter(1))[1]
final = [(name, count / float(max_count))for name, count in final]
final.pop(0) # remove "working"
final.pop(0) # remove "opening"
print final
word_cloud = WordCloud(font_path="onts/Georgia.ttf",
    width=1280, height=800, max_words=50, stopwords=[])
word_cloud.fit_words(final)
word_cloud.to_file("result/5_question4.png")

# export to File
file_array = []
for row in final_text:
    temp_sentence = ""
    for sentence in row:
        temp_sentence = sentence + ", " + temp_sentence
    file_array.append(temp_sentence)
osha_data["Activities"] = pd.DataFrame(file_array)
osha_data.to_csv('result/5_question4.csv', index = False)
print("========DONE==========")
