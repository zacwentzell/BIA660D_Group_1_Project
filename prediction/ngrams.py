"""
More advanced n-gram models and more advanced selection of models
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
import numpy as np
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step2.csv')
data.head(3)
"""
Ok, so for features: 
We know we're using pre-review rating, restaurant price, review length, and mispelling count. 
For restaurant_type, we're going to change that\/we'll also remove restaurant_name as a predictive
variable (not really applicable to new restaurants). Finally, for the text, we're going to 
expand on our bag-of-words model by using lemmatization and TF-IDF for ngrams. 

Ok so instead of binning for the restaurant categories, we'll assign each one of them a normalized 
score based on average review rating for that category. For each restaurant (each of which may have
multiple categories) we average the scores of each of their categories to arrive at the restaurant's
"type_score" 
"""
restaurant_categories = pd.read_csv('../BIA660D_Group_1_Project/eda/type_data.csv')
restaurant_categories.sort_values(by='Average_Score', inplace=True, ascending=False)
restaurant_categories['Rank'] = range(1,len(restaurant_categories)+1)
restaurant_categories['Rank'] = restaurant_categories['Rank'].apply(lambda x: x / len(restaurant_categories)) #normalize
restaurant_categories
data['type_score'] = 0
for row_n in range(len(data)):
    raw_types = data['restaurant_type'][row_n]
    type_list = raw_types.strip("']").strip("['").split("', '")
    all_ranks = []
    for the_type in type_list:
        the_rank = restaurant_categories.iloc[np.where(restaurant_categories.iloc[:,0]==the_type)[0]]['Rank']
        all_ranks.append(the_rank.values[0])
    data.loc[row_n, 'type_score'] = np.mean(all_ranks)
data.head(3)
data.drop(columns=['restaurant_name', 'restaurant_type'], inplace=True)
data.to_csv('../BIA660D_Group_1_Project/eda/hoboken_step3.csv', index = False) #yay!
#################################
import pandas as pd
import numpy as np
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step3.csv')
data.head(3)
"""Now for the hard part, the text.
Other feature ideas: 
# of /n in the text. (already mostly captured by review_length
# of mentions of restaurant's name in text. (hard to work with weird names, mispellings, abbreviations, etc.) 
"""
# Cleaning Text (basic)
import re, string
# Define Regex
apostrophes = re.compile("'")
punctuation = re.compile('[%s]' % re.escape(string.punctuation)) # all punctuation marks, but not escape characters i.e \n
large_num_newline = re.compile('[0-9]{2,}|\n+')
multiple_spaces = re.compile(' +')
def clean(text):
    text = apostrophes.sub('', text)
    text = punctuation.sub(' ', text)
    text = large_num_newline.sub(' ', text) #couldn't find any examples that had \n, but for saftey including this
    return( multiple_spaces.sub(' ', text).strip() )
# Select Text
texts = data['user_text']
texts = texts.apply(clean)
texts.head(3)
# Tokenize + stem text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import EnglishStemmer # A good one, also turns the text lowercase
# from nltk import word_tokenize # word_list = [word_tokenize(x) for x in texts] #seems slightly slower
word_list = list(map(str.split, texts)) # 75480 unique words
stemmer = EnglishStemmer(ignore_stopwords=True)
stemmed_word_list = list(map(lambda x: [stemmer.stem(w) for w in x], word_list)) #takes a while #41876 unique lemmas
stemmed_list = list(map(lambda x: ' '.join(x), stemmed_word_list))
tfidf = TfidfVectorizer(lowercase=True, stop_words='english', strip_accents='ascii', norm=None, ngram_range=(1,2),#1,2-grams
                        use_idf=False, max_df=0.99, min_df=0.01, sublinear_tf=True) #sublinar becasue it makes sense
# Ok I guess here is where we break up our datasets.
from sklearn.model_selection import train_test_split
texts1, texts2, data1, data2 = train_test_split(stemmed_list, data, test_size=0.2, random_state=1) #20% good percent?
tfidf.fit(texts1)
# len(set([item for sublist in stemmed_word_list for item in sublist]))#sum(word_list, [])
len(tfidf.vocabulary_) #912 terms
# Now transform into tf_idf's
tf1 = pd.DataFrame(tfidf.transform(texts1).toarray(), index=data1.index)
tf2 = pd.DataFrame(tfidf.transform(texts2).toarray(), index=data2.index)
y_train = data1['user_rating']
y_test = data2['user_rating']
data1.drop(columns=['user_rating', 'user_text'], inplace=True)
data2.drop(columns=['user_rating', 'user_text'], inplace=True)
x_train = pd.concat([data1, tf1], axis=1)
x_test = pd.concat([data2, tf2], axis=1)
# Ok now normalization to 0 mean and unit variance (robust for things like neural networks)
from sklearn.preprocessing import StandardScaler
normalizer = StandardScaler()
normalizer.fit(x_train.values) #not needed for output values
x_train_norm = pd.DataFrame(normalizer.transform(x_train), columns=x_train.columns, index=x_train.index)
x_test_norm = pd.DataFrame(normalizer.transform(x_test), columns=x_test.columns, index=x_test.index)
#
# x_train_norm.to_csv('../BIA660D_Group_1_Project/prediction/x_train_norm.csv', index=True)
# x_test_norm.to_csv('../BIA660D_Group_1_Project/prediction/x_test_norm.csv', index=True)
# y_train.to_csv('../BIA660D_Group_1_Project/prediction/y_train.csv', index=True)
# y_test.to_csv('../BIA660D_Group_1_Project/prediction/y_test.csv', index=True)
x_train_norm.to_pickle('../BIA660D_Group_1_Project/prediction/x_train_norm')
x_test_norm.to_pickle('../BIA660D_Group_1_Project/prediction/x_test_norm')
y_train.to_pickle('../BIA660D_Group_1_Project/prediction/y_train')
y_test.to_pickle('../BIA660D_Group_1_Project/prediction/y_test')
####################### omg why did i never learn about pickles earlier in life, these are great
# Now for fitting them to models
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report, cohen_kappa_score, roc_auc_score
x_train_norm = pd.read_pickle('../BIA660D_Group_1_Project/prediction/x_train_norm')
x_test_norm = pd.read_pickle('../BIA660D_Group_1_Project/prediction/x_test_norm')
y_train = pd.read_pickle('../BIA660D_Group_1_Project/prediction/y_train')
y_test = pd.read_pickle('../BIA660D_Group_1_Project/prediction/y_test')
# pd.concat([y_train,y_test]).value_counts() #somewhat imbalanced
def multiclass_auc(true, pred, average="macro"):
    lb = LabelBinarizer()
    lb.fit(true)
    true = lb.transform(true)
    pred = lb.transform(pred)
    return roc_auc_score(true, pred, average=average)
def evaluate(model, show_all=True):
    try:
        y_pred = model.predict(x_test_norm)
    except:
        model.fit(x_train_norm, y_train)
        y_pred = model.predict(x_test_norm)
    train_acc   = model.score(x_train_norm, y_train)
    test_acc = model.score(x_test_norm, y_test)
    if show_all:
        print(classification_report(y_test, y_pred))
    print("ROC AUC: "+str(round(multiclass_auc(y_test, y_pred),4)))
    print("Cohen's Kappa: " + str(round(cohen_kappa_score(y_test, y_pred),4)))
    print("Training accuracy: "+str(round(train_acc*100,2))+"%, testing accuracy: "+str(round(test_acc*100,2))+"%")
from sklearn.ensemble import RandomForestClassifier #min_samples_leaf REALLY negatively impacts the performance
#max_features=None -> great testing accuracy, also 0.4 and higher
rfc = RandomForestClassifier(random_state=1, max_features=0.333, max_depth=20,
                             n_jobs=-1, n_estimators=50)
evaluate(rfc) #auc: 0.94, cohens: 0.92, test: 0.95  #good!
from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier(random_state=1, max_features=0.5, max_depth=28) #is this overfitting?
evaluate(dtc) #auc: 0.95, cohens: 0.93, test: 0.95 #good!
from sklearn.neural_network import MLPClassifier #validation_fraction=0.1,#default, is good #150
# For the neural network, lets apply grid search to uncover optimal parameters
from sklearn.model_selection import GridSearchCV
# nnc = MLPClassifier(random_state=1) #early_stopping=False, hidden_layer_sizes=(100,)
# nn_gs = GridSearchCV(nnc, n_jobs=3, param_grid={'hidden_layer_sizes': [(50,), (100,), (150,), (200,)], 'early_stopping': [True, False]})
#hard to use GridSearch, takes forever, and it searched based on accuracy/other metrics on the training data, not on test data #nn_gs.fit(x_train_norm, y_train)
####\/Best Network I could achieve (based on cohen's cappa, AUC, and testing accuracy
nnc = MLPClassifier(random_state=1, early_stopping=True, hidden_layer_sizes=(150,), batch_size=200)
evaluate(nnc, show_all=False)#auc: 0.72, cohens: 0.46, test: 0.61
# ok that's no good, maybe if we oversampled it'd be better?
from sklearn.linear_model import LogisticRegression
#multiclass: solver='newton-cg', 'sag' (L1, fast), 'saga' (fast), 'lbfgs' #max_iter=100,  #multi_class='ovr', 'multinomial'
lr = LogisticRegression(random_state=1, n_jobs=-1, solver='lbfgs', multi_class='multinomial')  #best of all
evaluate(lr, show_all=False) #auc: 0.72, cohens: 0.45, test: 0.61
# logistic regression performed about as good as the neural network, wow
#As used by a blogger on Yelp review data
from sklearn.svm import LinearSVC #multi_class='crammer_singer'
svm = LinearSVC(random_state=1)
evaluate(svm, show_all=False) #auc: 0.68, cohens: 0.39, test: 0.56 #wow, bad
# nonlinar svm
from sklearn.svm import nusvc


""" 
multinomial Naive Bayes requires non-negative inputs (x), so due to my choice of normalization that's not an option.
"""

