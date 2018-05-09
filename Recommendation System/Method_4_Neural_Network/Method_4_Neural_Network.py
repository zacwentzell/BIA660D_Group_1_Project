from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import Normalizer
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

def normalize_variable(nn_df,variable_names):
    variables_li = []
    for variable in variable_names:
        variables_li.append(nn_df[variable])
    encoder = Normalizer()
    to_array = np.asarray(variables_li)
    norm_result = encoder.fit_transform(to_array)
    norm_result = norm_result.T
    return norm_result

stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer("[a-z']+")

def tokenize(text):
    tokens = tokenizer.tokenize(text)
    return [stemmer.stem(t) for t in tokens]

def get_tf(data, idf, max_df=1.0, min_df=1, ngram_range=(1,1)):
    if idf:
        """Convert a collection of raw documents to a matrix of TF-IDF features."""
        m = TfidfVectorizer(max_df=max_df, min_df=min_df, stop_words='english', ngram_range=ngram_range, tokenizer=tokenize,lowercase=True)
    d = m.fit_transform(data)
    return m, d

def get_nn_df(nn_df, norm_result, tfidf_d, variable_names):
    norm_result = pd.DataFrame(norm_result)
    tfidf_d = pd.DataFrame(tfidf_d.toarray())
    for index, name in enumerate(variable_names):
        tfidf_d[name] = norm_result.iloc[:,index]
    tfidf_d.index = nn_df.user_id
    tfidf_d['output'] = list(nn_df.restaurant_name)
    return tfidf_d

def get_recommendation_df(model, X_test):
    probability = model.predict_proba(X_test)
    recommendation_df = pd.DataFrame({'restaurant_name':model.classes_,'probability':probability[0]})
    return recommendation_df


def get_output(top_n, y_test,recommendation_df):
    top_n_df = recommendation_df[recommendation_df.restaurant_name != y_test].sort_values(by='probability', ascending=False).head(top_n)

    recommend_restaurant = list(top_n_df.loc[:,'restaurant_name'])
    recommend_score = list(top_n_df.loc[:,'probability'])
    recommendation_li = []
    for i in range(len(recommend_restaurant)):
        rank_restaurant_score = [str(i+1), recommend_restaurant[i], recommend_score[i]]
        recommendation_li.append(rank_restaurant_score)
    return recommendation_li

def store_the_recommendation(X_train, y_train,nn_df, top_n, nn_best):
    export_df = pd.DataFrame(nn_df.user_id)
    recommendation_li = []
    for i in range(len(X_train)):
        X_test = np.asarray(X_train.iloc[i, :])
        X_test = X_test.reshape(-1, 1).T
        y_test = y_train.iloc[i]
        recommendation_df = get_recommendation_df(nn_best, X_test)
        output = get_output(top_n, y_test, recommendation_df)
        recommendation_li.append(output)
        print(i)
    export_df['Recommendation'] = recommendation_li
    export_df.to_csv('Neural_Network_result.csv', index=False)
    return None

def main():
    df = pd.read_csv('Hoboken_restaurants_reviews_cleaned.csv')
    nn_df = df[
        ['user_id', 'restaurant_name', 'user_rating', 'restaurant_rating', 'restaurant_price', 'restaurant_type']]
    variable_names = ['user_rating', 'restaurant_rating', 'restaurant_price']
    norm_result = normalize_variable(nn_df, variable_names)

    tfidf_m, tfidf_d = get_tf(nn_df['restaurant_type'], idf=True, max_df=0.5, min_df=10)

    df = get_nn_df(nn_df, norm_result, tfidf_d, variable_names)
    df.to_csv('normalized_neural_network_dataset.csv')

    X_train = df.iloc[:, :-1]
    y_train = df.output

    nn = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(25, 6), random_state=1, learning_rate='adaptive', learning_rate_init= 0.005,
                       max_iter=1000)
    nn = nn.fit(X_train, y_train)

    top_n = 3

    store_the_recommendation(X_train, y_train, nn_df, top_n, nn)


if __name__ == '__main__':
    main()


