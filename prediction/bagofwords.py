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
logistic = LogisticRegression(solver='sag', random_state=1, max_iter=200)
logistic2 = LogisticRegression(solver='sag', random_state=1, max_iter=200)
logistic.fit(train_bow, train_ratings)
logistic2.fit(train_bigram, train_ratings)
log_bow_train = logistic.score(train_bow, train_ratings)
log_bow_test = logistic.score(test_bow, test_ratings)
log_bigram_train = logistic2.score(train_bigram, train_ratings)
log_bigram_test = logistic2.score(test_bigram, test_ratings)
print('Logistic Regression:')
print('BOW: train:'+per(log_bow_train)+', test:'+per(log_bow_test))
print('Bigram: train:'+per(log_bigram_train)+', test:'+per(log_bigram_test))
#Random Forest
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
rfc = RandomForestClassifier(random_state=1, n_estimators = 30) #n_estimators=10
rfc2 = RandomForestClassifier(random_state=1, n_estimators = 30) #n_estimators=10
rfc.fit(train_bow, train_ratings)
rfc2.fit(train_bigram, train_ratings)
rfc_bow_train = rfc.score(train_bow, train_ratings)
rfc_bow_test = rfc.score(test_bow, test_ratings)
rfc_bigram_train = rfc2.score(train_bigram, train_ratings)
rfc_bigram_test = rfc2.score(test_bigram, test_ratings)
print('Random Forest Classifier:')
print('BOW: train:'+per(rfc_bow_train)+', test:'+per(rfc_bow_test))
print('Bigram: train:'+per(rfc_bigram_train)+', test:'+per(rfc_bigram_test))
#Regressor
rfr = RandomForestRegressor(random_state=1, n_estimators=30)
rfr2 = RandomForestRegressor(random_state=1, n_estimators=30)
rfr.fit(train_bow, train_ratings)
rfr2.fit(train_bigram, train_ratings)
rfr_bow_train = rfr.score(train_bow, train_ratings)
rfr_bow_test = rfr.score(test_bow, test_ratings)
rfr_bigram_train = rfr2.score(train_bigram, train_ratings)
rfr_bigram_test = rfr2.score(test_bigram, test_ratings)
print('Random Forest Regressor:')
print('BOW: train:'+per(rfr_bow_train)+', test:'+per(rfr_bow_test))
print('Bigram: train:'+per(rfr_bigram_train)+', test:'+per(rfr_bigram_test))
## KNN ###
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
knc = KNeighborsClassifier()
knc2 = KNeighborsClassifier()
knc.fit(train_bow, train_ratings)
knc2.fit(train_bigram, train_ratings)
knc_bow_train = knc.score(train_bow, train_ratings)
knc_bow_test = knc.score(test_bow, test_ratings)
knc_bigram_train = knc2.score(train_bigram, train_ratings)
knc_bigram_test = knc2.score(test_bigram, test_ratings)
print('KNN Classifier:')
print('BOW: train:'+per(knc_bow_train)+', test:'+per(knc_bow_test))
print('Bigram: train:'+per(knc_bigram_train)+', test:'+per(knc_bigram_test))
#regressor
knr = KNeighborsRegressor()
knr2 = KNeighborsRegressor()
knr.fit(train_bow, train_ratings)
knr2.fit(train_bigram, train_ratings)
knr_bow_train = knr.score(train_bow, train_ratings)
knr_bow_test = knr.score(test_bow, test_ratings)
knr_bigram_train = knr2.score(train_bigram, train_ratings)
knr_bigram_test = knr2.score(test_bigram, test_ratings)
print('KNN Regressor:')
print('BOW: train:'+per(knr_bow_train)+', test:'+per(knr_bow_test))
print('Bigram: train:'+per(knr_bigram_train)+', test:'+per(knr_bigram_test))
### Decision Tree
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
dtc = DecisionTreeClassifier()
dtc2 = DecisionTreeClassifier()
dtc.fit(train_bow, train_ratings)
dtc2.fit(train_bigram, train_ratings)
dtc_bow_train = dtc.score(train_bow, train_ratings)
dtc_bow_test = dtc.score(test_bow, test_ratings)
dtc_bigram_train = dtc2.score(train_bigram, train_ratings)
dtc_bigram_test = dtc2.score(test_bigram, test_ratings)
print('Decision Tree Classifier:')
print('BOW: train:'+per(dtc_bow_train)+', test:'+per(dtc_bow_test))
print('Bigram: train:'+per(dtc_bigram_train)+', test:'+per(dtc_bigram_test))
# Regressor
dtr = DecisionTreeRegressor()
dtr2 = DecisionTreeRegressor()
dtr.fit(train_bow, train_ratings)
dtr2.fit(train_bigram, train_ratings)
dtr_bow_train = dtr.score(train_bow, train_ratings)
dtr_bow_test = dtr.score(test_bow, test_ratings)
dtr_bigram_train = dtr2.score(train_bigram, train_ratings)
dtr_bigram_test = dtr2.score(test_bigram, test_ratings)
print('Decision Tree Regressor:')
print('BOW: train:'+per(dtr_bow_train)+', test:'+per(dtr_bow_test))
print('Bigram: train:'+per(dtr_bigram_train)+', test:'+per(dtr_bigram_test))
# now for results table
models = ['NN_Classifier', 'NN_Regressor', 'SVM', 'PA_Classifier', 'PA_Regressor', 'Logistic',\
          'RF_Classifier', 'RF_Regressor', 'KNN_Classifier', 'KNN_Regressor', 'DT_Classifier', 'DT_Regressor']
results = [['Bag-of-Words Training', 'Bag-of-Words Test', 'Bag-of-Bigrams Training', 'Bag-of-Bigrams Test'],
           [nn_classifier_bow_train, nn_classifier_bow_test, nn_classifier_bigram_train, nn_classifier_bigram_test],
           [nn_regressor_bow_train, nn_regressor_bow_test, nn_regressor_bigram_train, nn_regressor_bigram_test],
           [svm_bow_train, svm_bow_test, svm_bigram_train, svm_bigram_test],
           [pac_bow_train, pac_bow_test, pac_bigram_train, pac_bigram_test],
           [par_bow_train, par_bow_test, par_bigram_train, par_bigram_test],
           [log_bow_train, log_bow_test, log_bigram_train, log_bigram_test],
           [rfc_bow_train, rfc_bow_test, rfc_bigram_train, rfc_bigram_test],
           [rfr_bow_train, rfr_bow_test, rfr_bigram_train, rfr_bigram_test],
           [knc_bow_train, knc_bow_test, knc_bigram_train, knc_bigram_test],
           [knr_bow_train, knr_bow_test, knr_bigram_train, knr_bigram_test],
           [dtc_bow_train, dtc_bow_test, dtc_bigram_train, dtc_bigram_test],
           [dtr_bow_train, dtr_bow_test, dtr_bigram_train, dtr_bigram_test]]
result_df = pd.DataFrame(results[1:], columns = results[0], index = models)
result_df.to_csv('../BIA660D_Group_1_Project/prediction/bagofwords.csv')
# result_df = pd.DataFrame.from_csv('../BIA660D_Group_1_Project/prediction/bagofwords.csv')
result_df
"""
Notes:

The SVM in question has a linear Kernal, and is based on 
http://www.developintelligence.com/blog/2017/03/predicting-yelp-star-ratings-review-text-python/

Classifier's have an advantage in terms of accuracy because the output is restricted to one of the valid options 
(int 1,2,3,4,5) regressors can be any number, it can result in numbers way outside the possible range of valid 
outcomes and it can also result in numbers within the range but not exactly equal to any valid number (like floats
between 1 and 2). Classifier accuracy can be judged based on whether or not they got the right value, with no partial
credit assigned for getting values close to it. Since it must be one out of 5 possible options, there's a chance of 
getting it right or getting an above average accuracy even with a weak predictor model. For the regressors, accuracy
is judged by R^2 which even allows for a negative accuracy (as happened with the Passive Aggressive regressor). 
we can't avoid this or alter the 'score' metric easily as sklearn does not allow alternate error metrics or scores
including Adjusted R^2 or MSE or something similar. A weak predicting regressor would likely have a very low chance 
of getting anywhere near the correct value without being part of some gradient boosting system. Therefore, even though
the classifiers outperformed the regressors accross-the-board in terms of score, if we take into account the scores and
the a priori notion that regressors allow for the linearity of features and the relation between ratings, then we should
accept a slightly lower score from a regressor as being comparable to a slightly higher score from a classifier on the 
same data. A notable comment to be made regarding the use of regressors is that the distance between the output labels
matters. On Yelp rating data in particular, it would make the implicit assumption that the difference between a 1-star
rating and a 2-star rating is the same as the difference between a 4-star and a 5-star rating and half the difference
between a 2-star and 4-star rating and so on. This is not necessarily the case as Yelp never claims that it is a 
perfectly linear scale and Yelp users do not use it as such. 

More information on this subject can be gleaned from examilning the distribution of Yelp review ratings and restauarant
ratings in our other EDA files, the ratings are not normally distributed, nor are they distributed in a way where one
could assume a priori that they are a linear function. Review ratings have a negative skew, and are highly concentrated
at the ratings 4 and 5. Restaurant ratings also have a negative skew, but since they are a mean of a sample of the 
previously discussed distribution, they are much more concentrated, with high frequencies for 3 and 4 and negligible 
frequency for all other values. 
"""
# Best results in training from:
