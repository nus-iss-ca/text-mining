#!/usr/bin/env python

import nltk
import os
import json
import unicodedata
import string
import io
import pandas as pd
import textmining
import sklearn
import numpy as np
import collections
import operator

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import stem
from nltk.tokenize import word_tokenize as wt
from nltk.probability import FreqDist
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

class Util():

    def __init__(self):
        self.wnl = nltk.WordNetLemmatizer()
        self.stopwords = stopwords.words('english')

    # function to remove stopwords
    # input: text to remove stopword
    # output: text
    def remove_stopword(self, text):
        return " ".join(filter(lambda word: word not in self.stopwords, text.split()))

    # function to normalize text, remove all the encoding, escape and special characters
    # input: text 
    # output: text
    def normalize(self, text):
        ntext = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        return ntext

    # function to remove punctuation
    # input: text, transform character from_char to character to_char
    # output: text
    def remove_punctuation(self, text, from_char, to_char):
        text_nopunc = text.translate(string.maketrans(from_char, to_char), string.punctuation)
        return text_nopunc

    # function to lemma tokens
    # input: tbd
    # output: tbd
    def lemmatize(self, tokens):
        text_lem = " ".join([self.wnl.lemmatize(t) for t in tokens])
        return text_lem

    # function to pre-process text: unicode normalize, remove punctation, lower text, remove stopword
    # input: dataframe data, columns array
    # output: dataframe 
    def preprocessing(self, data, columns):
        result = pd.DataFrame(columns=columns)
        data = data.dropna()
        for c in columns:
            for index, row in data.iterrows():
                if isinstance(row[c],int):
                    print str(index) + "----" + str(row[c])
                else:
                    temp = self.normalize(row[c])
                    temp = self.remove_punctuation(temp, "","")
                    temp = temp.lower()
                    temp = self.remove_stopword(temp)
                    result.loc[index, c] = temp
        
        return result.dropna()

    # function to do POS tag
    # input: dataframe, columns array, tag array
    def pos_tag(self, data, columns, tag):
        result = pd.DataFrame(columns=columns)
        data = data.dropna()
        result.title = data.title
        for index, row in data.iterrows():
            if not isinstance(row['summary'], int):
                temp = self.normalize(row['summary'])
                pos = pos_tag(wt(temp))
                temp = " ".join(noun[0] for noun in pos if noun[1] in tag)
                result.loc[index, 'summary'] = unicode(temp)
        # for c in columns:
        #     for index, row in data.iterrows():
        #         if not isinstance(row[c], int):
        #             temp = self.normalize(row[c])
        #             pos = pos_tag(wt(temp))
        #             temp = " ".join(noun[0] for noun in pos if noun[1] in tag)
        #             result.loc[index, c] = unicode(temp)
        return result.dropna()

    # function to create word clouds
    # input: tbd
    # output: tbd
    def create_wordclouds(self):
        return True

    # function to train SVM
    # input: vectors tfidf, data, parameter for C, gamma and kernel
    # output: svm model
    def train_svm(vectors, data, C, gamma, kernel):
        svm = SVC(C=C, gamma=gamma, kernel=kernel)
        svm.fit(vectors, data)
        return svm

    # def convert_pd_to_text(self, df):
    #     temp = pd.DataFrame()
    #     columns = list(df.column.values)
    #     for c in columns:
            
    #     result = pd.concat([df, df['bar'].dropna()]).reindex_like(df)

class Construction():
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def get_construction_category(self, string):
        result = []
        for word in string:
            if word in self.dictionary:
                result.append('Construction')
            else:
                result.append('Others')
        return result

    # data: dataframe
    def identify_construction(self, data):
        return True