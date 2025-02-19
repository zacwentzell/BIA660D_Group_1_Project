"""
Clean and EDA the Hoboken review data
BIA660D - Group 1: Alec Kulakowski
"""
# Import Statements
import pandas as pd
# import matplotlib.pyplot as plt #dont run this in pycharm
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step1.csv')
# data.drop(columns=data.columns[0], inplace=True)
# Deal with missing data
data['restaurant_rating'].fillna(data['restaurant_rating'].mean(), inplace=True)
data.head(2)
# Explore distribution of
# data['restaurant_rating'].plot(type='')
rating_distribution = data['user_rating'].value_counts().loc[list(range(1,6))]
def clean_types(x):
    x = x.replace("'", "")
    x = x.replace("[", "").replace("]", "")
    x = x.split(', ')
    return(x)
data['restaurant_type'] = data['restaurant_type'].map(clean_types)
data.head(2)
all_types = set()
x = data['restaurant_type'].apply(all_types.update)
# type_data = pd.Series(index=list(all_types))
# for type in list(all_types): # warning: Takes a LONG time
#     cumsum = 0
#     count = 0
#     for row_n in range(len(data)):
#         row = data.iloc[row_n]
#         if type in row['restaurant_type']:
#             cumsum = cumsum + row['user_rating']
#             count = count + 1
#     type_data[type] = cumsum/count
# type_data.head()
# type_data.to_csv('../BIA660D_Group_1_Project/eda/type_data.csv', index=True)
# type_data.to_csv('../BIA660D_Group_1_Project/eda/type_data.csv', index=True, header=['Average_Score'])
type_data = pd.DataFrame.from_csv('../BIA660D_Group_1_Project/eda/type_data.csv')
type_data.head(3)
type_data.sort_values(by='Average_Score')