# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 13:46:20 2018

@author: danis
"""


import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt


#this is the place to aet the numbers in order to display a full large dataframe
# in the ipython console a clear table. double clicking on the console
# will open it up on all screen
# in this case it shows first and last three columns
#small tables can be fully shown nicely with the to_string() function as shown below
#print(data["class_size"].to_string())
pd.set_option('display.max_columns',6)
#pd.set_option('display.max_colwidth',2)
pd.set_option('display.width',200)

def read_files_into_dict(file_path,file_name,data):
    df = pd.read_csv(file_path + '\\' + file_name)
    data[file_name[:-4]] = df #without .csv
    return data
    
data = {}
path = 'C:\\Python\\Exercise\\Files\\Schools'
files = ['ap_2010.csv','class_size.csv','demographics.csv','graduation.csv','hs_directory.csv','sat_results.csv']
for f in files:
    read_files_into_dict(path,f,data)
    
print(data.keys())

print()
print(data['class_size'].columns)

for k,df in data.items():
    print()
    print(k)
    print(df.head(5))
    

all_survey = pd.read_csv('C:\\Python\\Exercise\\Files\\Schools\\survey_all.txt',delimiter="\t",encoding="windows-1252")
d75_survey = pd.read_csv('C:\\Python\\Exercise\\Files\\Schools\\survey_d75.txt',delimiter="\t",encoding="windows-1252")    
survey = pd.concat([all_survey,d75_survey],sort='False',axis=0)
print()
#concat adds rows but also adds and merges columns
print(all_survey.shape) 
print(d75_survey.shape)
print(survey.shape)
#print(survey.head(5))


# filter and keep only a specific list of columns with loc[]
survey = survey.loc[:,["dbn", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]]
survey["DBN"] = survey["dbn"]
print()
print(survey.shape)
data["survey"] = survey


data['hs_directory']['DBN'] = data['hs_directory']['dbn'] 


#Create a DBN for class_size that has the same format of the other files
def pad_csd_two_digits(col):
    s = str(col)
    return s.zfill(2)

data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd_two_digits)
data["class_size"]['DBN'] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]

print()
print(data["class_size"].head(2))


print(data['sat_results']['SAT Critical Reading Avg. Score'].head(50))


#The original scores have string values for sowme rows, the to_numeric(errors="coerce") will turn them to Nan
# and then in the add up, the Nans will be ignored
cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pd.to_numeric(data["sat_results"][c], errors="coerce")
    #print(data["sat_results"][c].head(50))

data['sat_results']['sat_score'] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]
print(data['sat_results']['sat_score'].head())


print()
print(data['sat_results']['sat_score'])

print()
print(data['sat_results']['sat_score'].head(5))


# get latitude coordinate from location 1 column
def get_latitude(col):
    #regexp returns list - take first item, split it and then take first item again. finally ignore first char
    return re.findall("\(.+\)",col)[0].split(',')[0][1:] 


def get_longtitude(col):
    return re.findall("\(.+\)",col)[0].split(',')[1].replace(')','').strip()

data['hs_directory']['lat'] = data['hs_directory']['Location 1'].apply(get_latitude)
print()
#print(data['hs_directory'].head(50))

data['hs_directory']['long'] = data['hs_directory']['Location 1'].apply(get_longtitude)


#convert coord values to floats
data['hs_directory']['lat'] = pd.to_numeric(data['hs_directory']['lat'],errors="coerce")
data['hs_directory']['long'] = pd.to_numeric(data['hs_directory']['long'],errors="coerce")

print()
print(data['hs_directory'].head(50))

print(data['hs_directory']['long'])

#check if DBN are unique in columns
print()
print(data['sat_results']['DBN'].is_unique) #here they are unique
print(data['class_size']['DBN'].is_unique) #here not

print(data["class_size"].columns)


#filter values to make DBN more unique
class_size = data["class_size"][data["class_size"]['GRADE '] == '09-12']
print()
print(class_size)

class_size = class_size[class_size['PROGRAM TYPE'] == 'GEN ED']
print()
print(class_size)

#Group by and aggregate avarage of rows according to DBN 
class_size = class_size.groupby("DBN").agg(np.mean)
class_size.reset_index(inplace=True)


#check if DBN is now unique
print()
print(class_size['DBN'].is_unique) #now unique
data["class_size"] = class_size

# DBN unique ?
data['demographics'] = data['demographics'][data['demographics']['schoolyear'] == 20112012]

print()
print(data['demographics']['DBN'].is_unique)


# DBN unique ?
data['graduation'] = data['graduation'][(data['graduation']['Cohort'] == 2006) & (data['graduation']['Demographic'] == 'Total Cohort')]

print()
print(data['graduation']['DBN'].is_unique)

cols = ['AP Test Takers ','Total Exams Taken','Number of Exams with scores 3 4 or 5']
for c in cols:
    data['ap_2010'][c] = pd.to_numeric(data['ap_2010'][c], errors="coerce")
    
print()
print(data['ap_2010'].dtypes)


#merge all datsets to one dataset called combine - differnt merge stratergies exist
combined = data["sat_results"]
print()
print(combined.shape)
combined = combined.merge(data['ap_2010'],how='left',on='DBN')
print()
print(combined.shape)

combined = combined.merge(data['graduation'],how='left',on='DBN')
print()
print(combined.shape)

cols = ['class_size','demographics','survey','hs_directory']
for c in cols:
    combined = combined.merge(data[c],how='inner',on='DBN')
    
print()
print(combined.shape)

combined = combined.fillna(combined.mean()).fillna(0)

print()
print(combined)
print()


def extract_two_chars(col):
    return col[:2]

combined['school_dist'] = combined['DBN'].apply(extract_two_chars)

#Use the pandas.DataFrame.corr() method on the combined dataframe 
#to find all possible correlations
correlations = combined.corr()
print()
print(correlations)

#get the correlations of sat_score only, with cols that are not null 
#and sort the results desc
correlations = correlations.loc[:,'sat_score']
correlations[correlations.notnull()].sort_values(ascending=False)

#Create a scatterplot of total_enrollment versus sat_score.
combined.plot.scatter(x="total_enrollment", y="sat_score")


low_enrollment = combined[(combined["total_enrollment"] < 1000) & (combined['sat_score'] < 1200)]

low_enrollment.plot.scatter(x="total_enrollment", y="sat_score")

print()
print(low_enrollment['School Name'])


combined.plot.scatter(x="ell_percent", y="sat_score")


