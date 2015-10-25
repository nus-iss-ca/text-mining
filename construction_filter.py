from lib.util import *
import pandas as pd

dummy_data = pd.read_csv("data/super_scraped.csv")
list_id =[]
for index, row in dummy_data.iterrows():
	if row['industry'] == "ERROR":
		print index
	elif int(row['industry']) in range(1500,1800):
		list_id.append(row['id']) 

osha_data = pd.read_excel("data/osha.xlsx")
osha_data.columns = ['id', 'title', 'summary']

temp = pd.DataFrame()
for i in list_id:
	temp = osha_data[osha_data['id'] == i]

print temp