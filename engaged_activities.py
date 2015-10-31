# Find common activites that the victims were engaged in prior to the accident?
# import library
from lib.util import *
import re

util = Util()
#load data
osha_data = pd.read_csv("result/osha_filter.csv")
osha_data.columns = ['id', 'title', 'summary']
#
# #pos tag data, only get verb as the activites
# pattern = "(was|were ([\w]*).*)"

temp_summary = []
for index, row in osha_data.iterrows():
    # print("===========================================")
    # print row["summary"]
    # m = re.findall(r'was([^.]*).', row["summary"])
    m = re.findall(r'was ([^.]*).', row["summary"])
    n = re.findall(r'were ([^.]*).', row["summary"])
    # print("------------------------------------------")
    # print m
    # print n
    temp_summary = temp_summary + m + n
    # break
    # if m:
    #     temp_summary.append(m.groups())
    #     break
# print temp_summary

pos_array = []
for summary in temp_summary:
    temp_pos = pos_tag(wt(summary))
    temp_sentence = " ".join(word[0] for word in temp_pos if word[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
    pos_array.append(temp_sentence)
print pos_array

final_text = []
for sentence in pos_array:
    # temp_text = util.normalize(sentence)
    temp_text = util.remove_punctuation(sentence, "", "")
    temp_text = temp_text.lower()
    temp_text = util.remove_stopword(temp_text)
    temp_tokens = wt(temp_text)
    temp_text = util.lemmatize(temp_tokens)
    final_text.append(temp_text)

combine_text = " ".join(word for word in final_text)
temp_wordcloud = util.create_wordclouds(combine_text, "Activities", [], 180, 1280, 800)
print temp_wordcloud

word_frequency = FreqDist()
for word in final_text:
    word_frequency.inc(word)



# osha_pos_data = util.pos_tag(osha_data, ['title', 'summary'], ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
# osha_pos_data.to_csv('result/osha_pos_data.csv', index=False)
# osha_pos_data = pd.read_csv("result/osha_pos_data.csv")
#osha_data_processed = util.preprocessing(osha_data, ['title', 'summary'])

# osha_combine_text = " ".join(i for i in  osha_data['summary'])
# temp = util.create_wordclouds(osha_combine_text, "Activities", [], 180, 1280, 800)
# for item in temp:
#     print item[0]
# osha_tokens = wt(util.lemmatize(wt(osha_combine_text)))
#
# #count word
# word_frequency = FreqDist()
# for word in osha_tokens:
#     word_frequency.inc(word)
dictionary = []
i = 0
for word, freq in word_frequency.iteritems():
    dictionary.append([word,freq])
    i = i + 1
    if i == 100:
        break
print dictionary
