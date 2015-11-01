# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 11:51:56 2015

@author: Jasmine
"""

import os
import pandas as pd
import numpy as np

os.chdir("C:\\Users\\Jasmine\\Desktop\\TextMining\\CA\\Archive")

df = pd.read_csv("5_question4.csv")
df = df.astype(str)

df_edit = []
for index, row in df.iterrows():
    if row['Activities'] != "nan":
        temp = row['Activities'].split(",")
        for term in temp:
            term = term.strip()
            df_edit.append([row['id'],term])
    
df_edit = pd.DataFrame(df_edit, columns=['id','Activities'])
df_edit.to_csv("osha_activities.csv")

df_occupation = pd.read_csv("4_question3.csv")
df_occupation = df_occupation.astype(str)
df_occupation = df_occupation[['id','Occupation']]

df_object = pd.read_csv("3_question2.csv")
df_object = df_object.astype(str)
df_object = df_object[['id','Objects2']]

df_cause = pd.read_csv("osha_classified.csv")
df_cause = df_cause.astype(str)
df_cause = df_cause[['id','final_pred']]

result = pd.merge(df_cause, df_object,on='id')
result = pd.merge(result, df_occupation,on='id')

result.to_csv("osha_cause_occupation_object.csv")

result = pd.merge(result, df_edit,on='id')

result.to_csv("osha_cause_occupation_object_activities.csv")