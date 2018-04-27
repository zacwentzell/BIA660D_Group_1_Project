import pandas as pd
import numpy as np
from sklearn.decomposition import NMF


def get_matrix(file_name):
    df = pd.read_csv(file_name)
    matrix =np.matrix(df.iloc[:,1:])
    return matrix

def get_features_matrix(matrix):
    k_model = NMF(n_components=5, init='random', random_state=0)
    W = k_model.fit_transform(matrix)
    H = k_model.components_
    return W, H

def get_recommender_df(df, W, H):
    predict_matrix = np.matrix(np.dot(W,H))
    result_df = pd.DataFrame(predict_matrix)
    result_df.columns = df.columns[1:]
    result_df.insert(0, 'user_id', df.iloc[:, 0])
    return result_df

def export_result(df, result_df, top_n):
    recommendation_li = []
    for i in range(len(result_df)):
        attended_res_li = None
        try:
            attended_res_li = list(df.iloc[i, 1:][df.iloc[i, 1:] != 0].index)
        except:
            pass
        if attended_res_li is not None:
            for res in attended_res_li:
                result_df.loc[i, res] = 0

        recommendation_top_n = list(result_df.iloc[i, 1:].sort_values(ascending=False).head(top_n).index)
        recommendation_li.append(recommendation_top_n)
        print(i)

    print('Done!')
    export_df = pd.DataFrame(df.user_id)
    export_df['Recommendation'] = recommendation_li
    export_df.to_csv('matrix_factorization_result.csv')

    return None

def main():
    file_name = 'Method_3_dataset.csv'
    matrix = get_matrix(file_name)
    U_ik, V_jk = get_features_matrix(matrix)
    df = pd.read_csv(file_name)
    result_df = get_recommender_df(df, U_ik, V_jk)
    export_result(df, result_df, 3)
    return None

if __name__ == '__main__':
    main()



