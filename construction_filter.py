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
l = []
for i in list_id:
	l.append(osha_data[osha_data['id'] == i])
temp = pd.concat(l)
temp = temp[temp.summary != 'InspectionOpen DateSICEstablishment Name']
temp = temp.drop_duplicates(cols='id', keep='last')
temp['summary'] = temp['summary'].map(lambda x: x.lstrip().rstrip())
temp.to_csv("result/osha_filter.csv", index = False)
