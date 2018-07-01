# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 07:31:31 2018

@author: dani shamir
"""

import pandas

food_info = pandas.read_csv('C:\\Python\\Exercise\\Files\\food_info.csv')
print(type(food_info))

first_twenty_rows = food_info.head(20)
print(first_twenty_rows)

num_rows = food_info.shape[0]
print(num_rows)

num_col = food_info.shape[1]
print(num_col)


# Series object representing the seventh row.
food_info.loc[6]
print()
print(food_info.loc[6])


two_col_df = food_info[['NDB_No','Cholestrl_(mg)']]
print()
print(two_col_df[:5])

#Select and display only the columns that use grams for measurement (that end with "(g)").

print()
gram_columns = [s for s in food_info.columns.tolist() if s.endswith('(g)')]
gram_df = food_info[gram_columns]

print()
print(gram_df.head(3))

grams_of_protein_per_gram_of_water = food_info['Protein_(g)']/food_info['Water_(g)']
milligrams_of_calcium_and_iron = food_info['Calcium_(mg)'] + food_info['Iron_(mg)']

print()
print(grams_of_protein_per_gram_of_water)


#formula to create a nutritional index:
initial_rating = 2*food_info['Protein_(g)'] - 0.75*food_info['Lipid_Tot_(g)']

#Normalize the values in the "Protein_(g)" column, and assign the result to normalized_protein.
#Normalize the values in the "Lipid_Tot_(g)" column, and assign the result to normalized_fat.

normalized_protein = (food_info['Protein_(g)'] - food_info['Protein_(g)'].min())/(food_info['Protein_(g)'].max() - food_info['Protein_(g)'].min())
normalized_fat = (food_info['Lipid_Tot_(g)'] - food_info['Lipid_Tot_(g)'].min())/(food_info['Lipid_Tot_(g)'].max() - food_info['Lipid_Tot_(g)'].min())

#new cols in food_info
food_info["Normalized_Protein"] = normalized_protein
food_info["Normalized_Fat"] = normalized_fat

food_info['Norm_Nutr_Index']  = 2*food_info['Normalized_Protein'] - 0.75*food_info['Normalized_Fat']

#display nutrition index of first five products in the dataframe
print()
print(food_info[['Shrt_Desc','Norm_Nutr_Index']].head(5))

#sort the data frame itself by Norm_Nutr_Index 
food_info.sort_values('Norm_Nutr_Index',inplace=True,ascending=False)

print()
print(food_info[['Shrt_Desc','Norm_Nutr_Index']].head(4))







