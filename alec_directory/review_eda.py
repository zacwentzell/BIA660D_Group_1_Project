### Review Data Exploratory Data Analysis

# Navigate into the correct project directory
import os
os.chdir('../BIA660D_Group_1_Project')
# Extract the review data from its .zip form
from zipfile import ZipFile
import pandas as pd
zf = ZipFile("Hoboken_restaurants_reviews.csv.zip")
validation = pd.read_csv(zf.open('Hoboken_restaurants_reviews.csv'))
validation.drop(columns=[0])
validation.head(3)

# zf = ZipFile("Hoboken_restaurants_reviews.csv.zip")
# validation = zf.read(zf.namelist()[0])
# import zipfile
# a = zipfile.ZipFile("Hoboken_restaurants_reviews.csv.zip", "r")
# a.infolist()[0]
# a.infolist()
# a.namelist()
# a.open(a.infolist()[0])