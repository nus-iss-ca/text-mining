# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:34:41 2015

@author: Jasmine
"""

from lib.util import *

util = Util()

#################START SCRIPT######################
"""
This section of the code looks at the evaluation of the different
learning models

It is found that the ensemble model works best and hence will be used
for prediction cause of accident using osha data
"""

#read data
m_df = pd.read_csv("data/MsiaAccidentCases_edited.csv")

#clean data
m_df_temp = m_df
lem_text = m_df['Title Case'].tolist()
#lem_text = m_df['Summary Case'].tolist()
cleaned_train=[]

for i in lem_text:
    text_lower = util.remove_punctuation(i, "", "").lower()
    stop = stopwords.words('english')
    text_nostop = " ".join(filter(lambda word: word not in stop, text_lower.split()))
    tokens = word_tokenize(text_nostop)
    wnl = nltk.WordNetLemmatizer()
    text_lem=" ".join([wnl.lemmatize(t) for t in tokens])
    #tokens_lem = word_tokenize(text_lem)
    cleaned_train.append(text_lem)

m_df['lem_text'] = cleaned_train

svm_score = []
nb_score = []
dt_score =[]
kn_score =[]
lr_score=[]
em_score=[]

counter = 1
fold = int(len(m_df.index)/10)

for counter in range(1,11):

    lr = (counter-1)* fold
    hr = ((counter)*fold)-1

    if counter == 10:
        hr = len(m_df.index) - 1

    #create train and test set for 10 fold cross validation
    m_df_test = m_df[lr:hr]
    m_df_train = m_df[~m_df.index.isin(m_df_test.index)]

    # Create your Vectorizer function
    vectorizer = TfidfVectorizer()

    # Create TF-IDF Vectorizer from your training features
    train_vectors = vectorizer.fit_transform(m_df_train['lem_text'])
    # Transform your test features to fit your already trained TF-IDF
    test_vectors = vectorizer.transform(m_df_test['lem_text'])

    # Train the SVM
    sv = util.train_svm(train_vectors, m_df_train['Cause '], C = 5000.0, gamma= 0.0, kernel = 'rbf')

    # Predict on the Test set using the trained SVM
    predSVM = sv.predict(test_vectors)
    pred = list(predSVM)

    # SVM Accuracy Score
    svm_score.append(accuracy_score(pred, m_df_test['Cause ']))

# Can also create a Naive Bayes classifier using sklearn

    clf = MultinomialNB().fit(train_vectors, m_df_train['Cause '])
    predNB = clf.predict(test_vectors)
    pred = list(predNB)
    nb_score.append(accuracy_score(pred, m_df_test['Cause ']))

    # Decision Tree Classifier
    dt = util.train_dtc(train_vectors, m_df_train['Cause '])
    predDT = dt.predict(test_vectors)
    pred = list(predDT)
    dt_score.append(accuracy_score(pred, m_df_test['Cause ']))

    # K-Nearest Neighbours Classifier
    kn = util.train_knn(train_vectors, m_df_train['Cause '], 1, 'distance')
    predKN = kn.predict(test_vectors)
    pred = list(predKN)
    kn_score.append(accuracy_score(pred, m_df_test['Cause ']))

    # Logistic Regression Classifier
    lr = util.train_lr(train_vectors, m_df_train['Cause '])
    predLR = lr.predict(test_vectors)
    pred = list(predLR)
    lr_score.append(accuracy_score(pred, m_df_test['Cause ']))

    #Emsemble - pick majority vote. if no majority vote, grab svm prediction
    emsumble_df = pd.DataFrame(predDT,columns = ['predDT'])
    emsumble_df['predKN'] = predKN
    emsumble_df['predLR'] = predLR
    emsumble_df['predNB'] = predNB
    emsumble_df['predSVM'] = predSVM

    count_cat = pd.DataFrame(emsumble_df[emsumble_df =='Caught in/between Objects'].count(axis=1),columns = ['Caught in/between Objects'])
    count_cat['Other'] = emsumble_df[emsumble_df =='Other'].count(axis=1)
    count_cat['Struck By Moving Objects'] = emsumble_df[emsumble_df =='Struck By Moving Objects'].count(axis=1)
    count_cat['Fires and Explosion'] = emsumble_df[emsumble_df =='Fires and Explosion'].count(axis=1)
    count_cat['Falls'] = emsumble_df[emsumble_df =='Falls'].count(axis=1)
    count_cat['Electrocution'] = emsumble_df[emsumble_df =='Electrocution'].count(axis=1)
    count_cat['Exposure to extreme temperatures'] = emsumble_df[emsumble_df =='Exposure to extreme temperatures'].count(axis=1)
    count_cat['Collapse of object'] = emsumble_df[emsumble_df =='Collapse of object'].count(axis=1)
    count_cat['Exposure to Chemical Substances'] = emsumble_df[emsumble_df =='Exposure to Chemical Substances'].count(axis=1)
    count_cat['Drowning'] = emsumble_df[emsumble_df =='Drowning'].count(axis=1)
    count_cat['Suffocation'] = emsumble_df[emsumble_df =='Suffocation'].count(axis=1)
    count_cat['Max'] = count_cat.idxmax(axis=1)

    pred = list(count_cat['Max'])
    em_score.append(accuracy_score(pred, m_df_test['Cause ']))

print 'SVM accuracy: ' + str(sum(svm_score)/len(svm_score))
print 'NB accuracy: ' + str(sum(nb_score)/len(nb_score))
print 'DT accuracy: ' + str(sum(dt_score)/len(dt_score))
print 'KN accuracy: ' + str(sum(kn_score)/len(kn_score))
print 'LR accuracy: ' + str(sum(lr_score)/len(lr_score))
print 'Ensemble accuracy: ' + str(sum(em_score)/len(em_score))


#################START SCRIPT######################
"""
This section of the code looks classifying the cause of accidents using osha
data

This code will be run based on the list of identified construction data.
"""

#read data
m_df = pd.read_csv("data/MsiaAccidentCases_edited.csv")

#clean data
lem_text = m_df['Title Case'].tolist()

cleaned_train=[]

for i in lem_text:

    text_nopunc=i.translate(string.maketrans("",""), string.punctuation)
    text_lower=text_nopunc.lower()
    stop = stopwords.words('english')
    #stop = [k for k in stop if k not in ['no','nor','not','don','against','very','too']]
    #stop.extend(additional_stop_list)
    text_nostop=" ".join(filter(lambda word: word not in stop, text_lower.split()))
    tokens = word_tokenize(text_nostop)
    wnl = nltk.WordNetLemmatizer()
    text_lem=" ".join([wnl.lemmatize(t) for t in tokens])
    #tokens_lem = word_tokenize(text_lem)
    cleaned_train.append(text_lem)

m_df['lem_text'] = cleaned_train

# read osha data
o_df_test = pd.read_csv("result/1_osha_filter_scrapper.csv")
o_df_test = o_df_test[['id','title','summary']]
lem_text = o_df_test['title'].tolist()
lem_text = [str(x) for x in lem_text]

cleaned_train=[]

for i in lem_text:
    #text_nopunc=i.encode('utf-8').translate(string.maketrans("",""), string.punctuation)
    text_nopunc=i.translate(string.maketrans("",""), string.punctuation)
    text_lower=text_nopunc.lower()
    stop = stopwords.words('english')
    #stop = [k for k in stop if k not in ['no','nor','not','don','against','very','too']]
    #stop.extend(additional_stop_list)
    text_nostop=" ".join(filter(lambda word: word not in stop, text_lower.split()))
    tokens = word_tokenize(text_nostop)
    wnl = nltk.WordNetLemmatizer()
    text_lem=" ".join([wnl.lemmatize(t) for t in tokens])
    #tokens_lem = word_tokenize(text_lem)
    cleaned_train.append(text_lem)

o_df_test['lem_text'] = cleaned_train


m_df_train = m_df

# Create your Vectorizer function
vectorizer = TfidfVectorizer()

# Create TF-IDF Vectorizer from your training features
train_vectors = vectorizer.fit_transform(m_df_train['lem_text'])
# Transform your test features to fit your already trained TF-IDF
test_vectors = vectorizer.transform(o_df_test['lem_text'])

# Train the SVM
sv = util.train_svm(train_vectors, m_df_train['Cause '])

# Predict on the Test set using the trained SVM
predSVM= sv.predict(test_vectors)

# Can also create a Naive Bayes classifier using sklearn
clf = MultinomialNB().fit(train_vectors, m_df_train['Cause '])
predNB = clf.predict(test_vectors)

# Decision Tree Classifier
dt = util.train_dtc(train_vectors, m_df_train['Cause '])
predDT = dt.predict(test_vectors)

# K-Nearest Neighbours Classifier
kn = util.train_knn(train_vectors, m_df_train['Cause '], 1, 'distance')
predKN = kn.predict(test_vectors)

# Logistic Regression Classifier
lr = util.train_lr(train_vectors, m_df_train['Cause '])
predLR = lr.predict(test_vectors)

#Emsemble - pick majority vote. if no majority vote, grab svm prediction
emsumble_df = pd.DataFrame(predDT,columns = ['predDT'])
emsumble_df['predKN'] = predKN
emsumble_df['predLR'] = predLR
emsumble_df['predNB'] = predNB
emsumble_df['predSVM'] = predSVM

count_cat = pd.DataFrame(emsumble_df[emsumble_df =='Caught in/between Objects'].count(axis=1),columns = ['Caught in/between Objects'])
count_cat['Other'] = emsumble_df[emsumble_df =='Other'].count(axis=1)
count_cat['Struck By Moving Objects'] = emsumble_df[emsumble_df =='Struck By Moving Objects'].count(axis=1)
count_cat['Fires and Explosion'] = emsumble_df[emsumble_df =='Fires and Explosion'].count(axis=1)
count_cat['Falls'] = emsumble_df[emsumble_df =='Falls'].count(axis=1)
count_cat['Electrocution'] = emsumble_df[emsumble_df =='Electrocution'].count(axis=1)
count_cat['Exposure to extreme temperatures'] = emsumble_df[emsumble_df =='Exposure to extreme temperatures'].count(axis=1)
count_cat['Collapse of object'] = emsumble_df[emsumble_df =='Collapse of object'].count(axis=1)
count_cat['Exposure to Chemical Substances'] = emsumble_df[emsumble_df =='Exposure to Chemical Substances'].count(axis=1)
count_cat['Drowning'] = emsumble_df[emsumble_df =='Drowning'].count(axis=1)
count_cat['Suffocation'] = emsumble_df[emsumble_df =='Suffocation'].count(axis=1)
count_cat['Max'] = count_cat.idxmax(axis=1)

final_pred = list(count_cat['Max'])

o_df_test['final_pred'] = final_pred

o_df_test.to_csv('result/2_question1.csv')
