"""
Use bag-of-words to predict ratings.
BIA660D - Group 1: Alec Kulakowski
"""
# Imports
import pandas as pd
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step1.csv')
data.head(3)
# Bag-of-words, for now, we're just using text and no metadata
# data.drop(columns=['restaurant_name', 'restaurant_rating', 'restaurant_price', 'restaurant_type'], inplace=True)
# data.head(3)
reviews = data['user_text']
ratings = data['user_rating']
# Split the dataset into training and test data
from sklearn.model_selection import train_test_split
train_reviews, test_reviews, train_ratings, test_ratings = train_test_split(reviews, ratings, test_size=0.2, random_state=1)
# Vectorize using bag-of-words
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(strip_accents='ascii', stop_words='english', binary=True, max_df=0.9, max_features=1000)
vectorizer.fit(train_reviews)
# len(vectorizer.vocabulary_)
train_bow = vectorizer.transform(train_reviews)
test_bow = vectorizer.transform(test_reviews)
# Now with bag-of-bigrams
bigram_vectorizer = CountVectorizer(strip_accents='ascii', stop_words='english', binary=True, max_df=0.9, max_features=1000, ngram_range=(1,2))
bigram_vectorizer.fit(train_reviews)
len(bigram_vectorizer.vocabulary_)
train_bigram = bigram_vectorizer.transform(train_reviews)
test_bigram = bigram_vectorizer.transform(test_reviews)
# Now to fit models
from sklearn.neural_network import MLPClassifier, MLPRegressor
def per(x): return(str(round(100*x,2))+'%')
mlp = MLPClassifier(tol=0.0005, random_state=1)
mlp.fit(train_bow, train_ratings)
# Try with regressor
regressor = MLPRegressor(tol=0.0005, random_state=1)
regressor.fit(train_bow, train_ratings)
print('Bag-of-Words:')
print('Classifier Results: '+per(mlp.score(train_bow, train_ratings))+' training accuracy, '+per(mlp.score(test_bow, test_ratings))+' testing accuracy')
print('Regressor Results: '+per(regressor.score(train_bow, train_ratings))+' training accuracy, '+per(regressor.score(test_bow, test_ratings))+' testing accuracy')
# Oh, those results are sad, let's do it with bag-of-bigrams
mlp = MLPClassifier(tol=0.0005, random_state=1)
regressor = MLPRegressor(tol=0.0005, random_state=1)
mlp.fit(train_bigram, train_ratings)
regressor.fit(train_bigram, train_ratings)
print('Bag-of-Bigrams:')
print('Classifier Results: '+per(mlp.score(train_bigram, train_ratings))+' training accuracy, '+per(mlp.score(test_bigram, test_ratings))+' testing accuracy')
print('Regressor Results: '+per(regressor.score(train_bigram, train_ratings))+' training accuracy, '+per(regressor.score(test_bigram, test_ratings))+' testing accuracy')

