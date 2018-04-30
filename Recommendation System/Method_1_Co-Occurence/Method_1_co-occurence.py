import pandas as pd
import numpy as np


def get_dataset_co_occurence(df):
    # replace the rating with 1
    df = df.replace({5: 1, 4: 1, 3: 1, 2: 1})
    return df


def get_co_occurrence_matrices(co_occurence_dataset):
    co_matrices = np.matrix(co_occurence_dataset.iloc[:, 1:])
    co_matrices_t = co_matrices.getT()
    co_occurence_matrix = co_matrices_t * co_matrices
    np.fill_diagonal(co_occurence_matrix, 0)
    return co_occurence_matrix


def get_co_occurence_result(co_occurence_dataset, co_occurence_matrix, user_idx=None, user_id=None, top_n=None):
    ##input is index
    if user_idx is not None:
        user = co_occurence_dataset.iloc[user_idx, 1:]
    ##input is id
    if user_id is not None:
        user = co_occurence_dataset[co_occurence_dataset.user_id == user_id].iloc[0, 1:]

    ##convert Series to array
    user_vector = np.array(user)

    ##get co occurence recommender
    recommender = user_vector * co_occurence_matrix
    # matrix to array
    recommender = np.array(recommender).reshape(-1, )
    # array to list
    recommender = recommender.tolist()

    ##export the result list for one user
    # create result dataframe
    user_result = pd.DataFrame(user)
    # append recommender list to this result dataframe
    user_result['recommender'] = recommender

    # check if the user have already attended this restaurant
    # only rank the restaurant they did not attend
    result_for_user = user_result[user_result.iloc[:, 0] != 1].sort_values(by='recommender', ascending=False)

    # create recommendation list with n recommendations for each user
    result_for_user = list(result_for_user.head(top_n).index.values)
    return result_for_user


def store_result(co_occurence_dataset, co_occurence_matrix):
    # use for loop to get each user's recommendation list in the dataset
    recommendation_li = []
    for i in range(len(co_occurence_dataset)):
        recommendation_for_user = get_co_occurence_result(co_occurence_dataset, co_occurence_matrix, user_id=co_occurence_dataset.user_id[i], top_n=3)
        recommendation_li.append(recommendation_for_user)
        print(i)
    print('Done!')
    # create export dataset
    df = pd.read_csv('method_1_dataset.csv')
    # first column
    df = pd.DataFrame(df.user_id)
    # second column
    df['recommendation'] = recommendation_li
    # save
    df.to_csv('co_occurence_result.csv')
    return None

def main():
    df = pd.read_csv('method_1_dataset.csv')
    co_occurence_dataset = get_dataset_co_occurence(df)
    co_occurence_matrix = get_co_occurrence_matrices(co_occurence_dataset)
    store_result(co_occurence_dataset, co_occurence_matrix)


if __name__ == '__main__':
    main()


