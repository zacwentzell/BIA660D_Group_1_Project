import pandas as pd
import numpy as np


def get_co_occurrence_matrices(co_occurrence_dataset):
    # convert df to matix
    co_matrices = np.matrix(co_occurrence_dataset.iloc[:, 1:])

    # A.T
    co_matrices_t = co_matrices.getT()

    # co_occurrence matrix
    co_occurrence_matrix = co_matrices_t * co_matrices

    # ignore the diagonal cell and avoid to repeadedly calculate the restaurants the user have already attended
    np.fill_diagonal(co_occurrence_matrix, 0)
    return co_occurrence_matrix


def get_co_occurrence_result(co_occurrence_dataset, user_idx=None, user_id=None, top_n=None):
    """
    Args:

    co_occurrence_dataset: User and Items dataset
    co_occurrence_matrix:

    """

    ##input is index
    if user_idx is not None:
        user = co_occurrence_dataset.iloc[user_idx, 1:]
    ##input is id
    elif user_id is not None:
        user = co_occurrence_dataset[co_occurrence_dataset.user_id == user_id].iloc[0, 1:]

    ##convert Series to array
    user_vector = np.array(user)

    ##get co occurence recommender
    co_occurrence_matrix = get_co_occurrence_matrices(co_occurrence_dataset)
    recommender = user_vector * co_occurrence_matrix
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

    # create recommendation list with rating with n recommendations for each user
    result_for_user_restaurant = list(result_for_user.head(top_n).index.values)
    result_for_user_rating = list(result_for_user.recommender.head(top_n))
    recommend_restaurant_rating_li = []
    for i in range(len(result_for_user_restaurant)):
        recommend_rank_restaurant_rating = [str(i + 1), result_for_user_restaurant[i], result_for_user_rating[i]]
        recommend_restaurant_rating_li.append(recommend_rank_restaurant_rating)

    return recommend_restaurant_rating_li


def store_result(co_occurrence_dataset):
    # use for loop to get each user's recommendation list in the dataset
    co_occurrence_matrix = get_co_occurrence_matrices(co_occurrence_dataset)
    recommendation_li = []
    for i in range(len(co_occurrence_dataset)):
        # top_n = 3 according to the target of the project
        recommendation_for_user = get_co_occurrence_result(co_occurrence_dataset,
                                                           user_id=co_occurrence_dataset.user_id[i], top_n=3)
        recommendation_li.append(recommendation_for_user)
        print(i)

    print('get list!')
    # create output dataset
    df = pd.read_csv('Method_1_dataset.csv')
    # first column
    df = pd.DataFrame(df.user_id)
    # second column
    df['recommendation'] = recommendation_li
    # save
    df.to_csv('co_occurence_result.csv', index=False)
    return None

def main():
    co_occurrence_dataset = pd.read_csv('Method_1_dataset.csv')
    co_occurence_matrix = get_co_occurrence_matrices(co_occurrence_dataset)
    store_result(co_occurrence_dataset)


if __name__ == '__main__':
    main()


