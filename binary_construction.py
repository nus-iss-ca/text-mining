# Filter osha's accidents belong to contruction division

# load library, utilities
from lib.util import *
from collections import Counter

util = Util()
# load data
msia_data = pd.read_excel("data/MsiaAccidentCases.xlsx", "MsiaAccidentCases-cleaned")
msia_data.columns = ['cause', 'title', 'summary']
msia_columns = ['title', 'summary']

osha_data = pd.read_excel("data/osha.xlsx", "out_title")
osha_data.columns = ['id', 'title', 'summary']

# preprocessing data
msia_data_processed = util.preprocessing(msia_data, msia_columns)
msia_combine = msia_data_processed['title'] + " " +  msia_data_processed['summary']

# print msia_combine

msia_combine_text = " ".join(i for i in msia_combine)
msia_tokens = wt(util.lemmatize(wt(msia_combine_text)))
word_frequency = FreqDist()

for word in msia_tokens:
	word_frequency.inc(word)
i = 0
dictionary = []
for word, freq in word_frequency.iteritems():
	dictionary.append(word)
	i = i + 1
	if i == 1000:
		break

class_construction = Construction(dictionary)

osha_data_processed = util.preprocessing(osha_data, msia_columns)
osha_combine = osha_data_processed['title'] + " " + osha_data_processed['summary']
osha_combine.to_csv("temp.csv")
osha_combine = [wt(util.lemmatize(wt(text))) for text in osha_combine]
# osha_combine.to_csv("temp.csv")
print osha_combine

#osha_combine = pd.read_csv("temp.csv")
'''final_result = []
for index, string in osha_combine.iterrows():
	temp_array = class_construction.get_construction_category(string[1])
	counter = Counter(temp_array)
	if counter['Construction'] < 5:
		osha_data = osha_data.drop(index)

osha_data.to_excel('tuan.xlsx', index=False)'''

# print osha_combine


# from malaysia data, build dictionary for construction


# build model to predict osha is construction or not
# export to data file


# training = pd.read_csv("train.csv")
# col_list = ['year', 'primary_subject']
# timedf = training[col_list]
# train_pos = training[(training.Sentiment == 'positive')]
# train_pos_list = []
# for i,t in train_pos.iterrows():
#     train_pos_list.append([t.text.lower(), 1])
# for i in foreign_unclean.index:
#     foreign_unclean_abstract=foreign_unclean_abstract+str(foreign_unclean.abstract[i])

# actuals = pd.Series(actual)
# predicted = pd.Series(pred_list)

# # Print the confusion matrix
# pd.crosstab(actuals, predicted, rownames=['Actuals'], colnames=['Predicted'], margins=True)

# def neg_tag(text):
#     transformed = re.sub(r"\b(?:never|nothing|nowhere|noone|none|not|haven't|hasn't|hasnt|hadn't|hadnt|can't|cant|couldn't|couldnt|shouldn't|shouldnt|won't|wont|wouldn't|wouldnt|don't|dont|doesn't|doesnt|didn't|didnt|isnt|isn't|aren't|arent|aint|ain't|hardly|seldom)\b[\w\s]+[^\w\s]", lambda match: re.sub(r'(\s+)(\w+)', r'\1NEG_\2', match.group(0)), text, flags=re.IGNORECASE)
#     return(transformed)

# text_nopunc=foreign_abstract.translate(string.maketrans("",""), string.punctuation)
# text_lower=text_nopunc.lower()
# stop = stopwords.words('english')
# stop.extend(add)
# more_stop = open("long_stopwords.txt").read().splitlines()
# stop.extend(more_stop)
# text_nostop=" ".join(filter(lambda word: word not in stop, text_lower.split()))
# tokens = word_tokenize(text_nostop)
# wnl = nltk.WordNetLemmatizer()
# text_lem=" ".join([wnl.lemmatize(t) for t in tokens])
# textlem_nostop = " ".join(filter(lambda word: word not in stop, text_lem.split()))
# tokens_lem = word_tokenize(textlem_nostop)


# train_tokenized = [[wt(x), c] for x,c in train_set_neg]

# classifier = nltk.NaiveBayesClassifier.train(train_featureset)

# vectorizer = TfidfVectorizer()
# train_nolab = [t[0].decode('latin-1').encode("utf-8") for t in trainset]
# # Create TF-IDF Vectorizer from your training features
# train_vectors = vectorizer.fit_transform(train_nolab)
# train_lab = [t[1] for t in trainset]
# def train_svm(X, y):
#     """
#     Create and train the Support Vector Machine.
#     """
#     svm = SVC(C=5000.0, gamma=0.0, kernel='rbf')
#     svm.fit(X, y)
#     return svm

# # Train the SVM
# sv = train_svm(train_vectors, train_lab)
# train_vectors = vectorizer.fit_transform(train_nolab)

# bgm    = nltk.collocations.BigramAssocMeasures()
# finder = nltk.collocations.BigramCollocationFinder.from_words(tokens_lem,window_size=4)
# scored = finder.score_ngrams( bgm.jaccard  )

# # Group bigrams by first word in bigram.                                        
# prefix_keys = collections.defaultdict(list)
# for key, scores in scored:
#    prefix_keys[key[0]].append((key[1], scores))

# # Sort keyed bigrams by strongest association.                                  
# for key in prefix_keys:
#    prefix_keys[key].sort(key = lambda x: -x[1])

# print 'iraq', prefix_keys['iraq'][:5]
# print 'saddam', prefix_keys['saddam'][:5]

# # Calculate Unigram frequencies
# uni_freq = [(item, tokens_lem.count(item)) for item in sorted(set(tokens_lem))]

# # Calculate Bigram frequencies

# bgs = nltk.bigrams(tokens_lem)
# fdist = nltk.FreqDist(bgs)
# bi_freq = fdist.items()

# # Some minor bigram pre-processing for ease of use later
# temp1 = []
# for i in bi_freq:
#     big = i[0][0] + " " + i[0][1]
#     freq = i[1]
#     L = [big, freq]
#     temp1.append(L)


# # Convert into dict for ease of access in the function for pmi
# big_freq = dict(temp1)
# uni_freq = dict(uni_freq)

# # Create a function for pmi - just to calculate for bigrams. Consideration is that you need 
# # a list of unigram frequencies and bigram frequencies
# def pmi(word1, word2, uni_freq, bi_freq):
#     prob_word1 = uni_freq[word1]/float(sum(uni_freq.values()))
#     prob_word2 = uni_freq[word2]/float(sum(uni_freq.values()))
#     prob_word1_word2 = bi_freq[" ".join([word1,word2])]/float(sum(bi_freq.values()))
#     return log(prob_word1_word2/float(prob_word1*prob_word2),2)
    

# pmi("saddam", "hussein", uni_freq, big_freq)
# pmi("nigerian", "government", uni_freq, big_freq)
# # Remove NAs from the dataset
# amnesty_nona = amnesty.dropna(subset=['abstract'])

# # Create a list with all tokenized abstracts
# article_amnesty = []
# for i in amnesty_nona.index:
#     text = amnesty_nona.abstract[i]
#     text_nopunc=text.translate(string.maketrans("",""), string.punctuation)
#     text_lower=text_nopunc.lower()
#     text_nostop=" ".join(filter(lambda word: word not in stop, text_lower.split()))
#     tokens = word_tokenize(text_nostop)
#     wnl = nltk.WordNetLemmatizer()
#     text_lem=" ".join([wnl.lemmatize(t) for t in tokens])
#     textlem_nostop = " ".join(filter(lambda word: word not in stop, text_lem.split()))
#     tokens_lem = word_tokenize(textlem_nostop)
#     tok=list(set(tokens_lem))
#     article_amnesty.append(tok)
    

# # Write the list into a csv
# with open("mba.csv", "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(article_amnesty)
