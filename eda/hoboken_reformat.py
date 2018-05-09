"""
Remove superfluous columns and rectify ratings
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
hoboken_raw = pd.read_csv('../BIA660D_Group_1_Project/scraping/hoboken_cleaned.csv')
hoboken_raw.head(2)
# Lets first move all user data, since this isn't the reccomendation system and user data would just help
# overfit the model.
hoboken_raw.drop(columns=['user_id', 'user_name'], inplace=True)
hoboken_raw.head(2)
# Now lets see if we can transform those restaurant ratings into ratings that are independent of the review in each
#row, thus they can be used as predictive variables without using look-ahead bias (although to completely avoid such
#bias, we'd need to know the mean review for the restaurant at the time of each review, which could be done manually
#post scraping if scraping had included review date or order.
restaurant_list = hoboken_raw['restaurant_name'].unique()
for restaurant in restaurant_list: # warning: Takes a LONG time
    review_indexes = hoboken_raw.loc[hoboken_raw['restaurant_name'] == restaurant].index
    review_count = len(review_indexes)
    superscore = review_count * hoboken_raw.iloc[review_indexes[0]]['restaurant_rating'] #could be improved
    for i in review_indexes:
        review = hoboken_raw.iloc[i]
        review.loc['restaurant_rating'] = (superscore - review['user_rating']) / (review_count - 1)
        hoboken_raw.iloc[i] = review
        print("Review #"+str(i)+" done.")
hoboken_raw.to_csv('../BIA660D_Group_1_Project/eda/hoboken_step1.csv', index=False)
#########################

# hoboken_raw.head()