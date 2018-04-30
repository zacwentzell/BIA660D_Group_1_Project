"""
Convert the scraped data from Hoboken into the same format as the Yelp Open Dataset data
BIA660D - Group 1: Alec Kulakowski
"""
# Navigate into the correct project directory
import os # os.listdir()
os.chdir('../BIA660D_Group_1_Project')
# Extract the review data from its .zip form
from zipfile import ZipFile
import pandas as pd
zf = ZipFile("Hoboken_restaurants_reviews.csv.zip")
raw = pd.read_csv(zf.open('Hoboken_restaurants_reviews.csv'))
validation = raw.copy()
validation = validation.drop(columns=validation.columns.values[0:2]) # Drop index columns
# Convert user_ratings from string to integer and restaurant ratings from string to float
validation['user_rating'] = validation['user_rating'].apply(lambda x: int(x[0]))
validation['restaurant_rating'] = validation['restaurant_rating'].apply(lambda x: float(x[0:3]))
# Display price distribution
print(validation['restaurant_price'].value_counts())
# Display number of absent prices
print('Missing prices: '+str(validation['restaurant_price'].isnull().sum()))
# Replace missing values with mean and convert to integer
def try_convert(x, y=0):
    try: return(x.count('$'))
    except: return(y)
average_price = sum(validation['restaurant_price'].apply(lambda x: try_convert(x))) / validation['restaurant_price'].value_counts().sum()
validation['restaurant_price'] = validation['restaurant_price'].apply(lambda x: try_convert(x, y=average_price))
# Separate Restaurant Type
# from sklearn.feature_extraction import DictVectorizer
# dv = DictVectorizer(sparse=False)
# dv.fit_transform()
type_list = validation['restaurant_type'].str.split(', ').str.join(' ').str.split(',')
# type_list = validation['restaurant_type'].str.split('[,]+[ ]+')
type_list = type_list.apply(lambda l: [w.strip() for w in l])
# Clean specific errors in listed types
def clean_type(types):
    for i in range(len(types)):
        if types[i]=='Deliswfftdfvzztzaxqcuvwesssrrqrbsuxbfedbtd':
            types[i] = 'Delis'
        elif types[i]=='Japanesetdassttaucfxffdddaerfstets':
            types[i] = 'Japanese'
        elif types[i]=='Beer Barawsuvqvreabrdbevr':
            types[i] = 'Beer Bar'
    return types # can't be done inplace?
type_list = type_list.apply(lambda x: clean_type(x))
all_types = list(set(x for l in type_list for x in l))
# Alter original DataFrame
validation = validation.drop(columns=['restaurant_type'])
# type_df = pd.DataFrame(columns=all_types, index=validation.index)
# for row in range(len(validation)):
#     for type_index in range(len(all_types)):
#         if all_types[type_index] in type_list[row]:
#             type_df[all_types[type_index]][row] = 1
#         else:
#             type_df[all_types[type_index]][row] = 0
dict_rows = []
for row_index in validation.index:
    this_row = validation.loc[row_index].to_dict()
    for value in type_list.loc[row_index]:
        this_row[value] = 1
    dict_rows.append(this_row)
validation = pd.DataFrame(dict_rows)
validation.loc[:, all_types] = validation.loc[:, all_types].fillna(0)
# validation.loc[:, all_types].fillna(0, inplace=True) # wasn't working
# Now EDA, professor reccomends using SVD for the restaurant types

validation.head(2)
raw.head(2)
#test

#is this really clean?
clean = pd.read_csv('Recommendation System/Hoboken_restaurants_reviews_cleaned.csv')
clean.head(2)
type(clean.loc[0]['restaurant_type']) #is str, should be list w/3  items

# dict_rows = []
# for row_index in validation.index:
#     this_row = validation.loc[row_index].to_dict()
#     for value in type_list.loc[row_index]:
#         this_row[value] = 1
#     dict_rows.append(this_row)
# temp = pd.DataFrame(dict_rows).fillna(0)
# len(temp.columns) - len(validation.columns) - len(all_types) == 0 # True
# a = temp.iloc[0]
# a[:-len(validation.columns)].sum() # 2
# len(type_list.iloc[0]) # 3
# temp.head(3)

# temp[['Wine Bars', 'Italian', 'Cocktail Bars']].head(3)
#
# for x in type_list.iloc[0]:
#     temp
#
# temp.head(3)
#
# type_df.head(3)
# type_list.head(3)
# a = [x for x in validation.itertuples()]
# b = a[0]
#
#
# b = a[:3]
# b.unique()
# a.str.encode('base64', 'strict')
# validation.head(3)
#
# from sklearn import preprocessing
# le = preprocessing.LabelEncoder()
# le.fit(all_types)
#
# from sklearn import preprocessing
# lb = preprocessing.LabelBinarizer()
# v = DictVectorizer(sparse=False)
# from sklearn.preprocessing import OneHotEncoder
# enc = OneHotEncoder()
# enc.fit([['me', 'you'], ['you', 'i']])
# enc = preprocessing.OneHotEncoder(n_values=[2, 3, 4])
#
# b = validation.itertuples()
# a = [x for x in b]
# a[5271:5274]
# w = a[0]
# w.__getattribute__('restaurant_price')
# # for a in validation.itertuples():
# #     # print(a)
# #     if a.__getattribute__('restaurant_price') is None:
# #     # if a['restaurant_price'].isnull():
# #         print(a)
# # validation['restaurant_price'].isnull().sum()
# # validation['restaurant_price'].apply(lambda x: x.count('$'))
# # validation.head(3)