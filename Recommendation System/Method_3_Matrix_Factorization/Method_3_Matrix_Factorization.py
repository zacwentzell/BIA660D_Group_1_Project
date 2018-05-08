import pandas as pd
import numpy as np
from sklearn.decomposition import NMF


def get_matrix(file_name):
    df = pd.read_csv(file_name)
    matrix =np.matrix(df.iloc[:,1:])
    return matrix

def get_features_matrix(matrices, features_no):
    k_model = NMF(n_components=features_no, init='random', random_state=0)
    W = k_model.fit_transform(matrices)
    H = k_model.components_
    return W, H

def get_recommender_df( W, H):
    df = pd.read_csv('Method_3_dataset.csv')
    predict_matrix = np.matrix(np.dot(W,H))
    result_df = pd.DataFrame(predict_matrix)
    result_df.columns = df.columns[1:]
    result_df.insert(0, 'user_id', df.iloc[:, 0])
    return result_df

def remove_attended_restaurant(result_df):
    df = pd.read_csv('Method_3_dataset.csv')
    for i in range(len(df)):
        attended_res_li = None
        attended_res_li = list(df.iloc[i, 1:][df.iloc[i, 1:] != 0].index)
        for res in attended_res_li:
            result_df.loc[i, res] = 0
    print('Remove Attended Restaurant!')
    return None


def recommend_for_user(result_df, top_n, idx=None, user_id=None):
    if idx is not None:
        recommend_restaurant = list(result_df.iloc[idx, 1:].sort_values(ascending=False).head(top_n).index)
        recommend_scores = list(result_df.iloc[idx, 1:].sort_values(ascending=False).head(top_n))
    elif user_id is not None:
        recommend_restaurant = list(
            result_df[result_df.user_id == user_id].iloc[0, 1:].sort_values(ascending=False).head(top_n).index)
        recommend_scores = list(
            result_df[result_df.user_id == user_id].iloc[0, 1:].sort_values(ascending=False).head(top_n))
    else:
        print('Unknown Error!')

    recommend_rank_restaurant_scores_li = []
    for i in range(len(recommend_restaurant)):
        item = [str(i + 1), recommend_restaurant[i], recommend_scores[i]]
        recommend_rank_restaurant_scores_li.append(item)

    return recommend_rank_restaurant_scores_li

def export_result(result_df):
    recommendation_li = []
    for i in range(len(result_df)):
        recommend_for_each_user = recommend_for_user(result_df, top_n=3, idx=i, user_id=None)
        recommendation_li.append(recommend_for_each_user)
        print(i)
    print('Done!')
    export_df = pd.DataFrame(result_df.user_id)
    export_df['Recommendation'] = recommendation_li
    export_df.to_csv('matrix_factorization_result.csv')
    return None

def main():
    file_name = 'Method_3_dataset.csv'
    matrices = get_matrix(file_name)
    U_ik, V_jk = get_features_matrix(matrices, 10)
    result_df = get_recommender_df(U_ik, V_jk)
    remove_attended_restaurant(result_df)
    export_result(result_df)
    return None

if __name__ == '__main__':
    main()



