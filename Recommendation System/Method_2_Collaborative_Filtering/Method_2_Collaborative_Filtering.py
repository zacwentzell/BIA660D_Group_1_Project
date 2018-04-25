import pandas as pd
import graphlab
from sklearn.model_selection import train_test_split


df = pd.read_csv('Method_2_dataset.csv')
train_data, test_data = train_test_split(df, test_size=0.25)
train_data_gl = graphlab.SFrame(train_data)
test_data_gl = graphlab.SFrame(test_data)


Cosine_model = graphlab.item_similarity_recommender.create(train_data_gl, user_id='user_id',
                                                             item_id='restaurant_name',
                                                             target='user_rating',
                                                             similarity_type='cosine')

Jaccard_model = graphlab.item_similarity_recommender.create(train_data_gl, user_id='user_id',
                                                             item_id='restaurant_name',
                                                             target='user_rating',
                                                             similarity_type='jaccard')

Cosine_recommendation = Cosine_model.recommend(k=3,verbose=False)
Cosine_recommendation.save('Cosine_recommendation_result.csv')

Jaccard_recommendation = Jaccard_model.recommend(k=3,verbose=False)
Cosine_recommendation.save('Jaccard_recommendation_result.csv')