# Filter osha's accidents belong to contruction division

# load library, utilities
from lib.util import *
from collections import Counter
import csv

util = Util()
# load data
msia_data = pd.read_excel("data/MsiaAccidentCases.xlsx", "MsiaAccidentCases-cleaned")
msia_data.columns = ['cause', 'title', 'summary']
msia_columns = ['title','summary']

osha_data = pd.read_excel("data/osha.xlsx", "out_title")
osha_data.columns = ['id', 'title', 'summary']

# preprocessing data
#, 'NNP', 'NNPS', 'PRP', 'PRP$']
msia_pos_data = util.pos_tag(msia_data, msia_columns, ['NN', 'NNS'])
msia_data_processed = util.preprocessing(msia_pos_data, msia_columns)
msia_combine = msia_data_processed['title'] + " " +  msia_data_processed['summary']

# # print msia_combine

msia_combine_text = " ".join(i for i in  msia_data_processed['summary'])
msia_tokens = wt(util.lemmatize(wt(msia_combine_text)))
msia_pos = pos_tag(msia_tokens)

word_frequency = FreqDist()

for word in msia_tokens:
	word_frequency.inc(word)
i = 0
dictionary = []
for word, freq in word_frequency.iteritems():
	dictionary.append(word)
	i = i + 1
	if i == 200:
		break
# print dictionary

class_construction = Construction(dictionary)

# osha_data_processed = util.preprocessing(osha_data, msia_columns)
# osha_combine = osha_data_processed['title'] + " " + osha_data_processed['summary']

osha_combine = pd.read_csv("temp.csv")
# osha_combine = [wt(util.lemmatize(wt(text))) for text in osha_combine]

for index, row in osha_combine.iterrows():
	tmp = wt(util.lemmatize(wt(row[1])))
	temp_array = class_construction.get_construction_category(tmp)
	counter = Counter(temp_array)
	if counter['Construction'] < 20:
		osha_data = osha_data.drop(index)

osha_data.to_excel('tuan.xlsx', index=False)