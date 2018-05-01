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
data['restaurant_type'] = data['restaurant_type'].map(lambda x: x.replace("'",'').replace('[','').replace(']','').split(','))
all_types = set()
for types in data['restaurant_type']:

