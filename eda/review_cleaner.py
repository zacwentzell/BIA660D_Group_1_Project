"""
Clean the data from the review data import and prepare it for EDA
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
review_raw = pd.read_csv('../BIA660D_Group_1_Project/yelp_dataset/dataset/review.csv') #, nrows=100
review_raw.drop(columns = ['funny', 'useful', 'cool', 'review_id'], inplace=True)
# hoboken_raw = pd.read_csv('../BIA660D_Group_1_Project/scraping/hoboken_cleaned.csv', nrows=100) # TODO: Remove
businesses_raw = pd.read_csv('../BIA660D_Group_1_Project/yelp_dataset/dataset/business.csv') #, nrows=100
to_drop = list(businesses_raw.columns[1:75]) + list(businesses_raw.columns[76:82]) + list(businesses_raw.columns[84:92])
to_drop = to_drop + ['neighborhood', 'postal_code', 'state', 'latitude', 'longitude']
businesses_raw.drop(columns = to_drop, inplace=True) #for efficiency & other purposes
# hoboken_raw.head(1) # TODO: Remove
# businesses_raw.head(2)
new_data = []
review_count = len(review_raw)
print("Iterating through review data. Total of "+str(review_count)+" entries.")
for review_index in review_raw.index:
    review = review_raw.loc[review_index].to_dict()
    b_id = review['business_id']
    business = businesses_raw.loc[businesses_raw['business_id'] == b_id]
    b_name = business['name'].values[0]
    review['restaurant_name'] = b_name
    b_cat_raw = business['categories'].values[0].replace("'", '').replace("[", '').replace("]", '')
    b_cat = b_cat_raw.split(', ')
    review['restaurant_type'] = b_cat
    b_price = business['attributes.RestaurantsPriceRange2'].values[0]
    review['restaurant_price'] = b_price
    review['restaurant_reviews'] = business['review_count']
    # review['restaurant_open'] = business['is_open']
    review['restaurant_score'] = business['stars']
    new_data.append(review)
    print(str(review_index)+' out of '+str(review_count)+' reviews done.')
review_nt = pd.DataFrame(new_data)
print("Saving new file. ")
# review_nt['stars'].unique()
# review_nt['restaurant_price'].unique()
# # business.iloc[0].index.values
# business['attributes.RestaurantsPriceRange2'].values[0]
review_nt.to_csv('../BIA660D_Group_1_Project/yelp_dataset/dataset/review_new.csv')
# # TODO: Remove below
# review = review_raw.loc[0]
# b_id = review['business_id']
# business = businesses_raw.loc[businesses_raw['business_id'] == b_id]
# b_name = business['name']
# b_cat_raw = business['categories'].values[0].replace("'",'').replace("[",'').replace("]",'')
# b_cat = b_cat_raw.split(', ')
#
# businesses_raw.head(2)
# review_raw.head(2)
# businesses_raw.head(2)

