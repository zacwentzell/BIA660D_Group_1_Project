"""
More EDA and feature selection
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
import numpy as np
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step1.csv')
data.head(2)
# Lets see what correlations we can draw and what new features we can create
### Feature Evaluation
new_data = data.drop(np.where(data['restaurant_rating'].isnull())[0]) #just for the EDA
new_data['restaurant_rating'].isnull().sum() == 0
new_data['restaurant_rating'] = new_data['restaurant_rating'].apply(lambda x: round(x*2)/2)
# Lets look at a bar chart showing the variance present at various ratings
average_to_rating = new_data[['restaurant_rating', 'user_rating']] #obviously a correlation ofc # maybe just plot dispursion
# Relationship of restaurant cuisine type to rating?
type_to_ratings = pd.read_csv('../BIA660D_Group_1_Project/eda/type_data.csv')
type_to_ratings.sort_values(by='Average_Score', inplace=True)
# Relationship of review length to ratings?
data['review_len'] = data['user_text'].apply(len)
length_to_ratings = data[['review_len', 'user_rating']]
# Relationship of price to ratings?
price_to_ratings = data[['restaurant_price', 'user_rating']]
#
from autocorrect import spell #import re
spell('We booked Grand Vin')
spell(data['user_text'][0])
data['user_text'][0]



data.head(2)







