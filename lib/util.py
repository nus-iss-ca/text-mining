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
import image
import re

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import stem
from nltk.tokenize import word_tokenize as wt
from nltk.probability import FreqDist
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from wordcloud import WordCloud
# from pytagcloud import create_tag_image, make_tags, LAYOUTS

class Util():

    def __init__(self):
        self.wnl = nltk.WordNetLemmatizer()
        self.stopwords = stopwords.words('english')

    # function to remove stopwords
    # input: text to remove stopword
    # output: text
    def remove_stopword(self, text, stop = None):
        if stop == None:
            stop = self.stopwords
        return " ".join(filter(lambda word: word not in stop, text.split()))

    # function to normalize text, remove all the encoding, escape and special characters
    # input: text
    # output: text
    def normalize(self, text):
        # ntext = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        ntext = text.encode('ascii', 'ignore')
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
                    # temp = row[c]
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
                #temp = self.normalize(row['summary'].strip('#'))
                temp = row['summary']
                pos = pos_tag(wt(temp))
                temp = " ".join(noun[0] for noun in pos if noun[1] in tag)
                print temp
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
    def create_wordclouds(self, text, name_of_cloud, additional_stop_list, max_words, width, height, bigram = False):
        text_nopunc = self.remove_punctuation(text, "", "")
        text_lower = text_nopunc.lower()
        stop = self.stopwords
        stop.extend(additional_stop_list)
        text_nostop = self.remove_stopword(text_lower, stop)
        tokens = wt(text_nostop)
        text_lem = self.lemmatize(tokens)
        tokens_lem = wt(text_lem)
        my_bigrams = nltk.bigrams(tokens_lem)
        if bigram:
            bigram_merged=list()
            for line in my_bigrams:
                bigram_merged.append(line[0]+' ' + line[1])
            counts = collections.Counter(bigram_merged)
        else:
            counts = collections.Counter(tokens_lem)
        final = counts.most_common(max_words)
        max_count = max(final, key=operator.itemgetter(1))[1]
        final = [(name, count / float(max_count))for name, count in final]

        # tags = make_tags(final, maxsize=max_word_size)
        # create_tag_image(tags, name_of_cloud+'.png', size=(width, height), layout=3, fontname='Crimson Text', background = (255, 255, 255))

        # temp_cloud = " ".join(text for text, count in final)
        word_cloud = WordCloud(font_path="fonts/Georgia.ttf",
            width=width, height=height, max_words=max_words, stopwords=stop)
        word_cloud.fit_words(final)
        word_cloud.to_file(name_of_cloud + ".png")

    # function to train SVM
    # input: vectors tfidf, data, parameter for C, gamma and kernel
    # output: svm model
    def train_svm(vectors, data, C, gamma, kernel):
        svm = SVC(C=C, gamma=gamma, kernel=kernel)
        svm.fit(vectors, data)
        return svm

    # using dataframe to save array to file
    def save_array_to_file(self, array, path):
        temp_df = pd.DataFrame(columns = ["text"])
        for item in array:
            temp_df = temp_df.append({"text": item}, ignore_index = True)
        temp_df.to_csv(path, index = False)

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
