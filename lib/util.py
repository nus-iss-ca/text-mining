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

    def remove_stopword(data):


    def normalize(data):
        ntext = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        return ntext

    def remove_punctuation(data, punc):
        text_nopunc = ntext.translate(string.maketrans(punc), string.punctuation)
        return text_nopunc

    def lemmatize(tokens):
        text_lem = " ".join([self.wnl.lemmatize(t) for t in tokens])
        return text_lem

    def preprocessing(data):
        
