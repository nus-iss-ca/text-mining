# Find common activites that the victims were engaged in prior to the accident?
# import library
from lib.util import *
import re

util = Util()
#load data
osha_data = pd.read_csv("result/osha_filter.csv")
osha_data.columns = ['id', 'title', 'summary']

temp_summary = []
for index, row in osha_data.iterrows():
    m = re.findall(r'was ([^.]*).', row["summary"])
    n = re.findall(r'were ([^.]*).', row["summary"])
    temp_summary = temp_summary + m + n

# # print temp_summary
# util.save_array_to_file(temp_summary, "result/temp_summary.csv")
#
pos_array = []
# origin_pos = []
for summary in temp_summary:
    temp_pos = pos_tag(wt(summary))
    for i in range(0, len(temp_pos)):
        temp_sentence = ""
        temp_index = 0
        # if temp_pos[i][1] == "VBD":
        #     if (not i == len(temp_pos) - 1) and (temp_pos[i+1][1] in ["VB", "VBG", "VBN"]):
        #         for j in range(i+1, len(temp_pos)):
        #             temp_sentence = temp_sentence + " " + temp_pos[j][0]
        #             temp_index = temp_index + 1
        #             if temp_index == 4:
        #                 break
        #     else:
        #         for j in range(i, len(temp_pos)):
        #             temp_sentence = temp_sentence + " " + temp_pos[j][0]
        #             temp_index = temp_index + 1
        #             if temp_index == 4:
        #                 break
        # elif temp_pos[i][1] in ["VB", "VBG", "VBN"]:
        if temp_pos[i][1] == "VBG":
            for j in range(i, len(temp_pos)):
                temp_sentence = temp_sentence + " " + temp_pos[j][0]
                temp_index = temp_index + 1
                if temp_index == 4:
                    break
        if not temp_sentence == "":
            pos_array.append(temp_sentence.rstrip())
            print temp_sentence
    # temp_sentence = " ".join(word[0] for word in temp_pos if word[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    # pos_array.append(temp_sentence)
    # origin_pos.append(temp_pos)
# util.save_array_to_file(pos_array, "result/pos_array_selected.csv")
# util.save_array_to_file(origin_pos, "result/origin_pos.csv")
# temp_data = pd.read_csv("result/pos_array_selected.csv")
# for index, row in temp_data.iterrows():
#     text_nopunc = util.remove_punctuation(str(row["text"]), "", "")
#     text_lower = text_nopunc.lower()
#     # text_nostop = util.remove_stopword(text_lower)
#     tokens = wt(text_lower)
#     text_lem = util.lemmatize(tokens)
#     pos_array.append(text_lem)

final_text = []
for sentence in pos_array:
    # temp_text = util.normalize(sentence)
    temp_text = util.remove_punctuation(sentence, "", "")
    temp_text = temp_text.lower()
    # temp_text = util.remove_stopword(temp_text)
    temp_tokens = wt(temp_text)
    temp_text = util.lemmatize(temp_tokens)
    final_text.append(temp_text)
# util.save_array_to_file(final_text, "result/final_text.csv")
counts = collections.Counter(final_text)
counts += collections.Counter()
final = counts.most_common(100)
max_count = max(final, key=operator.itemgetter(1))[1]
final = [(name, count / float(max_count))for name, count in final]
final.pop(0)
# print final

# stop = util.stopwords
# stop.extend(["killed"])

word_cloud = WordCloud(font_path="/Library/Fonts/Georgia.ttf",
    width=1280, height=800, max_words=100, stopwords=[])
word_cloud.fit_words(final)
# # print final
word_cloud.to_file("Activities" + ".png")
# combine_text = " ".join(word for word in pos_array)
# util.create_wordclouds(combine_text, "Activities", ["nan"], 200, 1280, 800, False)

# word_frequency = FreqDist()
# for word in final_text:
#     word_frequency.inc(word)

# dictionary = []
# i = 0
# for word, freq in word_frequency.iteritems():
#     dictionary.append([word,freq])
#     i = i + 1
#     if i == 100:
#         break
# print dictionary
