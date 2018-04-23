### Review Data Exploratory Data Analysis

# Navigate into the correct project directory
import os # os.listdir()
os.chdir('../BIA660D_Group_1_Project')
# Extract the review data from its .zip form
from zipfile import ZipFile
import pandas as pd
zf = ZipFile("Hoboken_restaurants_reviews.csv.zip")
validation = pd.read_csv(zf.open('Hoboken_restaurants_reviews.csv'))
validation = validation.drop(columns=validation.columns.values[0:2]) # Drop index columns
# Convert user_ratings from string to integer
validation['user_rating'] = validation['user_rating'].apply(lambda x: int(x[0]))
# Display price distribution
print(validation['restaurant_price'].value_counts())
# Display number of absent prices
print('Missing prices: '+str(validation['restaurant_price'].isnull().sum()))
#
b = validation.itertuples()
a = [x for x in b]
w = a[0]
for a in validation.itertuples():
    # print(a)
    if a.__getattribute__('restaurant_price') is None:
    # if a['restaurant_price'].isnull():
        print(a)
validation['restaurant_price'].isnull().sum()
validation['restaurant_price'].apply(lambda x: x.count('$'))
validation.head(3) 