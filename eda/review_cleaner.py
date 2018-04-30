"""
Clean the data from the review data import and prepare it for EDA
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
from zipfile import ZipFile
review_raw = pd.read_csv('../BIA660D_Group_1_Project/yelp_dataset/dataset/review.csv')
zf = ZipFile("../BIA660D_Group_1_Project/Hoboken_restaurants_reviews.csv.zip")
raw = pd.read_csv(zf.open('Hoboken_restaurants_reviews.csv'))