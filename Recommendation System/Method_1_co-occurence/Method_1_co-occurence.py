import pandas as pd
import numpy as np

def get_dataset_co_occurence(df):
    df = df.replace({5:1, 4:1, 3:1, 2:1})
    return df

def get_co_occurrence_matrices(df):
    co_train_set = get_dataset_co_occurence(df)
    co_matrices =np.matrix(co_train_set.iloc[:,1:])
    co_matrices_t = co_matrices.getT()
    co_matrices_t
    co_occurence_matrix = co_matrices_t * co_matrices
    np.fill_diagonal(co_occurence_matrix, 0)
    return co_train_set,co_occurence_matrix

def get_co_occurence_result(df=None, user_idx=None, user_id = None, top_n=None):
    if user_idx is not None:
        user = co_train_set.iloc[user_idx,1:]
    if user_id is not None:
        user = co_train_set[co_train_set.user_id== user_id].iloc[0][1:]
    user_vector = np.array(user)
    recommender =  user_vector * co_occurence_matrix
    recommender = np.array(recommender).reshape(-1,)
    recommender = recommender.tolist()
    user_result = pd.DataFrame(user)
    user_result['recommender'] = recommender
    result_for_user = user_result[user_result.iloc[:, 0] != 1].sort_values(by = 'recommender', ascending = False)
    result_for_user = list(result_for_user.head(top_n).index.values)
    return result_for_user

def main():
    train_set = pd.read_csv('Method_1_dataset.csv')
    co_train_set, co_occurence_matrix = get_co_occurrence_matrices(train_set)
    recommendation_li = []
    for i in range(len(train_set)):
        recommendation_for_user = get_co_occurence_result(df=co_train_set, user_id=train_set.user_id[i], top_n=3)
        recommendation_li.append(recommendation_for_user)

    train_set = pd.DataFrame(train_set.user_id)
    train_set['Recommendation'] = recommendation_li
    train_set.to_csv('co_occurence_result.csv')
    return None

if __name__ == '__main__':
    main()


