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
from sklearn.feature_extraction import DictVectorizer
dv = DictVectorizer(sparse=False)
a = validation['restaurant_type'][0]
a
validation.head(3)



b = validation.itertuples()
a = [x for x in b]
a[5271:5274]
w = a[0]
w.__getattribute__('restaurant_price')
# for a in validation.itertuples():
#     # print(a)
#     if a.__getattribute__('restaurant_price') is None:
#     # if a['restaurant_price'].isnull():
#         print(a)
# validation['restaurant_price'].isnull().sum()
# validation['restaurant_price'].apply(lambda x: x.count('$'))
# validation.head(3)