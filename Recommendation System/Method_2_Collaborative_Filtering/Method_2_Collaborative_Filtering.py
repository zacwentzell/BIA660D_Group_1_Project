import pandas as pd
import graphlab
from sklearn.model_selection import train_test_split

def get_train_test(file_name):
    df = pd.read_csv(file_name)
    train_data, test_data = train_test_split(df, test_size=0.25)
    train_data_gl = graphlab.SFrame(train_data)
    test_data_gl = graphlab.SFrame(test_data)
    return train_data_gl, test_data_gl

def get_similarity_model(train, solver):
    if solver == 'cosine':
        Cosine_model = graphlab.item_similarity_recommender.create(train, user_id='user_id',
                                                                     item_id='restaurant_name',
                                                                     target='user_rating',
                                                                     similarity_type='cosine')
        model = Cosine_model
    elif solver == 'jaccard':
        Jaccard_model = graphlab.item_similarity_recommender.create(train, user_id='user_id',
                                                                     item_id='restaurant_name',
                                                                     target='user_rating',
                                                                    similarity_type='jaccard')
        model = Jaccard_model
    else:
        print('Unknown Error!')
    return model

def get_result(export_name, model, top_n=3):
    recommendation = model.recommend(k=top_n,verbose=False)
    recommendation.save(export_name)
    return None

def main():
    train, test = get_train_test('method_2_dataset.csv')
    #model = get_similarity_model(train, 'cosine')
    model = get_similarity_model(train, 'jaccard')

    #get_result('Cosine_recommendation_result.csv', model, 3)
    get_result('Jaccard_recommendation_result.csv', model, 3)
    return None

if __name__ == '__main__':
    main()
