import pandas as pd
import os 
f = '/Users/Tristan/Downloads/Uni/KnowledgeEngineering/CSV/Requirements.csv'

def read_csv(f, delim=','):
	'''opens a csv reader object'''
	# return csv.reader(open(f, 'r'), delimiter=delim)
	return pd.read_csv(f, sep=';', encoding = "ISO-8859-1", error_bad_lines=False) #index_col='pseudopatnummer'
	# return pd.read_csv(open(f, 'r'), sep=delim,encoding='latin-1')


student = os.path.splitext(os.path.split(f)[1])[0]
print(student)