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
validation.head(3) 