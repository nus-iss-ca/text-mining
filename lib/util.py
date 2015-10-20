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
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import stem
from sklearn.feature_extraction.text import CountVectorizer

class Util():

    def __init__(self):
        self.wnl = nltk.WordNetLemmatizer()

    # function to remove stopwords
    # input: tbd
    # output: tbd
    def remove_stopword(self, data):
        return True

    # function to normalize text, remove all the encoding, escape and special characters
    # input: tbd
    # output: tbd
    def normalize(self, data):
        ntext = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        return ntext

    # function to remove punctuation
    # input: tbd
    # output: tbd
    def remove_punctuation(self, data, punc):
        text_nopunc = ntext.translate(string.maketrans(punc), string.punctuation)
        return text_nopunc

    # function to lemma tokens
    # input: tbd
    # output: tbd
    def lemmatize(self, tokens):
        text_lem = " ".join([self.wnl.lemmatize(t) for t in tokens])
        return text_lem

    # function to pre-process text
    # input: tbd
    # output: tbd
    def preprocessing(self, data):
        return True

    # function to create word clouds
    # input: tbd
    # output: tbd
    def create_wordclouds(self):
        return True

