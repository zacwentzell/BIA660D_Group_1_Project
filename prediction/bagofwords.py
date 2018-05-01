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
train_reviews, test_reviews, train_ratings, test_ratings = train_test_split(reviews, ratings, test_size=0.15, random_state=1)
# Vectorize using bag-of-words
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(strip_accents='ascii', stop_words='english', binary=True, max_df=0.9, max_features=1000)
vectorizer.fit(train_reviews)
# len(vectorizer.vocabulary_)
train_bow = vectorizer.transform(train_reviews)
test_bow = vectorizer.transform(test_reviews)
# Now with bag-of-bigrams #ngram_range=(1,2) # changed to (2)
bigram_vectorizer = CountVectorizer(strip_accents='ascii', stop_words='english', binary=True, max_df=0.9, max_features=1000, ngram_range=(1,2))
bigram_vectorizer.fit(train_reviews)
len(bigram_vectorizer.vocabulary_)
train_bigram = bigram_vectorizer.transform(train_reviews)
test_bigram = bigram_vectorizer.transform(test_reviews)
### Now to fit models
from sklearn.neural_network import MLPClassifier, MLPRegressor
# Define parameters & misc functions
hyperparameters = {'tol': 0.005, 'hidden_layer_sizes': (250, 100, 50), 'random_state': 1}
def per(x): return(str(round(100*x,2))+'%')
mlp = MLPClassifier(**hyperparameters)
mlp.fit(train_bow, train_ratings)
# Try with regressor
# regressor = MLPRegressor(tol=tolerance, hidden_layer_sizes=network_shape, random_state=r)
regressor = MLPRegressor(**hyperparameters)
regressor.fit(train_bow, train_ratings)
# Record and desplay results
nn_classifier_bow_train = mlp.score(train_bow, train_ratings)
nn_classifier_bow_test = mlp.score(test_bow, test_ratings)
nn_regressor_bow_train = regressor.score(train_bow, train_ratings)
nn_regressor_bow_test = regressor.score(test_bow, test_ratings)
print('Bag-of-Words:')
print('Classifier Results: '+per(mlp.score(train_bow, train_ratings))+' training accuracy, '+per(mlp.score(test_bow, test_ratings))+' testing accuracy')
print('Regressor Results: '+per(regressor.score(train_bow, train_ratings))+' training accuracy, '+per(regressor.score(test_bow, test_ratings))+' testing accuracy')
# Oh, those results are sad, let's do it with bag-of-bigrams
mlp2 = MLPClassifier(**hyperparameters)
regressor2 = MLPRegressor(**hyperparameters)
mlp2.fit(train_bigram, train_ratings)
regressor2.fit(train_bigram, train_ratings)
# Record and desplay results
nn_classifier_bigram_train = mlp2.score(train_bigram, train_ratings)
nn_classifier_bigram_test = mlp2.score(test_bigram, test_ratings)
nn_regressor_bigram_train = regressor2.score(train_bigram, train_ratings)
nn_regressor_bigram_test = regressor2.score(test_bigram, test_ratings)
print('Bag-of-Bigrams:')
print('Classifier Results: '+per(mlp2.score(train_bigram, train_ratings))+' training accuracy, '+per(mlp2.score(test_bigram, test_ratings))+' testing accuracy')
print('Regressor Results: '+per(regressor2.score(train_bigram, train_ratings))+' training accuracy, '+per(regressor2.score(test_bigram, test_ratings))+' testing accuracy')
# Now lets try using an SVM
from sklearn.svm import LinearSVC
svm = LinearSVC()
svm2 = LinearSVC()
svm.fit(train_bow, train_ratings)
svm2.fit(train_bigram, train_ratings)
# Record and desplay results
svm_bow_train = svm.score(train_bow, train_ratings)
svm_bow_test = svm.score(test_bow, test_ratings)
svm_bigram_train = svm2.score(train_bigram, train_ratings)
svm_bigram_test = svm2.score(test_bigram, test_ratings)
print('SVM Results:')
print('BOW Results: '+per(svm_bow_train)+' training accuracy, '+per(svm_bow_test)+' testing accuracy')
print('Bigram Results: '+per(svm_bigram_train)+' training accuracy, '+per(svm_bigram_test)+' testing accuracy')
# Now lets try using passive aggressive classifier:
from sklearn.linear_model import PassiveAggressiveClassifier, PassiveAggressiveRegressor
pac = PassiveAggressiveClassifier()
pac2 = PassiveAggressiveClassifier()
par = PassiveAggressiveRegressor()
par2 = PassiveAggressiveRegressor()
# Now fit
pac.fit(train_bow, train_ratings)
par.fit(train_bow, train_ratings)
pac2.fit(train_bigram, train_ratings)
par2.fit(train_bigram, train_ratings)
# Record and desplay results
pac_bow_train = pac.score(train_bow, train_ratings)
pac_bow_test = pac.score(test_bow, test_ratings)
pac_bigram_train = pac2.score(train_bigram, train_ratings)
pac_bigram_test = pac2.score(test_bigram, test_ratings)
par_bow_train = par.score(train_bow, train_ratings)
par_bow_test = par.score(test_bow, test_ratings)
par_bigram_train = par2.score(train_bigram, train_ratings)
par_bigram_test = par2.score(test_bigram, test_ratings)
# Results
print('Passive Aggressive Classifier')
print('BOW Results: '+per(pac_bow_train)+' training accuracy, '+per(pac_bow_test)+' testing accuracy')
print('Bigram Results: '+per(pac_bigram_train)+' training accuracy, '+per(pac_bigram_test)+' testing accuracy')
print('Passive Aggressive Regressor')
print('BOW Results: '+per(par_bow_train)+' training accuracy, '+per(par_bow_test)+' testing accuracy')
print('Bigram Results: '+per(par_bigram_test)+' training accuracy, '+per(par_bigram_test)+' testing accuracy')
# Lets try linear
from sklearn.linear_model import LogisticRegression
logistic = LogisticRegression(solver='sag', random_state=1, max_iter=500)
logistic2 = LogisticRegression(solver='sag', random_state=1, max_iter=500)
logistic.fit(train_bow, train_ratings)
logistic2.fit(train_bigram, train_ratings)
log_bow_train = logistic.score(train_bow, train_ratings)
log_bow_test = logistic.score(test_bow, test_ratings)
log_bigram_train = logistic2.score(train_bigram, train_ratings)
log_bigram_test = logistic2.score(test_bigram, test_ratings)
print('BOW: train:'+per(log_bow_train)+', test:'+per(log_bow_test))
print('Bigram: train:'+per(log_bigram_train)+', test:'+per(log_bigram_test))

# now for results table
models = ['NN_Classifier', 'NN_Regressor', 'SVM', 'PA_Classifier', 'PA_Regressor']
results = [['Bag-of-Words Training', 'Bag-of-Words Test', 'Bag-of-Bigrams Training', 'Bag-of-Bigrams Test'],
           [nn_classifier_bow_train, nn_classifier_bow_test, nn_classifier_bigram_train, nn_classifier_bigram_test],
           [nn_regressor_bow_train, nn_regressor_bow_test, nn_regressor_bigram_train, nn_regressor_bigram_test],
           [svm_bow_train, svm_bow_test, svm_bigram_train, svm_bigram_test],
           [pac_bow_train, pac_bow_test, pac_bigram_train, pac_bigram_test],
           [par_bow_train, par_bow_test, par_bigram_train, par_bigram_test]]
result_df = pd.DataFrame(results[1:], columns = results[0], index = models)
result_df
# Best results in training from: