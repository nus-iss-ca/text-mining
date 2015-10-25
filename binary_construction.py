# Filter osha's accidents belong to contruction division

# load library, utilities
from lib.util import *
from collections import Counter
import csv

util = Util()
# load data
# --load msia data
msia_data = pd.read_excel("data/MsiaAccidentCases.xlsx", "MsiaAccidentCases-cleaned")
msia_data.columns = ['cause', 'title', 'summary'] # rename columns
msia_columns = ['title','summary']
# --load osha data
osha_data = pd.read_excel("data/osha.xlsx", "out_title")
osha_data.columns = ['id', 'title', 'summary'] # rename columns

# preprocessing msia data
msia_pos_data = util.pos_tag(msia_data, msia_columns, ['NN', 'NNS']) # POS tag and select only noun in data
msia_data_processed = util.preprocessing(msia_pos_data, msia_columns) # normalize, remove punctuation and stopwords, lower text
msia_combine = msia_data_processed['title'] + " " +  msia_data_processed['summary'] # merge title and summary

msia_combine_text = " ".join(i for i in  msia_data_processed['summary']) # combine all rows to 1 single text
msia_tokens = wt(util.lemmatize(wt(msia_combine_text))) # tokenize this text

# build dictionary from msia based on word frequency
word_frequency = FreqDist()
# --count frequency of words
for word in msia_tokens:
	word_frequency.inc(word)
# --create dictionary array based on most n frequency words
i = 0
dictionary = []
for word, freq in word_frequency.iteritems():
	dictionary.append(word)
	i = i + 1
	if i == 200:
		break
# --create classifier based on dictionary to identify class Construction or not
class_construction = Construction(dictionary)

# apply classifier to osha data
# --preprocessing osha data
# osha_data_processed = util.preprocessing(osha_data, msia_columns)
# osha_combine = osha_data_processed['title'] + " " + osha_data_processed['summary']

# --for testing purpose, load csv file will faster than process whole data everytime run the code
osha_combine = pd.read_csv("temp.csv")
# osha_combine = [wt(util.lemmatize(wt(text))) for text in osha_combine]

# --count words' class (Construction/Other) in each row, if row has at least 20 words belong to Construction class, save it
for index, row in osha_combine.iterrows():
	tmp = wt(util.lemmatize(wt(row[1]))) # tokenize string before assign class to each word
	temp_array = class_construction.get_construction_category(tmp)
	counter = Counter(temp_array)
	if counter['Construction'] < 20:
		osha_data = osha_data.drop(index)

osha_data.to_excel('data/osha-construction.xlsx', index=False)