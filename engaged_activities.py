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
    print("===========================================")
    print row["summary"]
    m = re.findall(r'was([^.]*).', row["summary"])
    print("------------------------------------------")
    print m
    break
    # if m:
    #     temp_summary.append(m.groups())
    #     break
# print temp_summary


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
# dictionary = []
# i = 0
# for word, freq in word_frequency.iteritems():
#     dictionary.append([word,freq])
#     i = i + 1
#     if i == 100:
#         break
# print dictionary
