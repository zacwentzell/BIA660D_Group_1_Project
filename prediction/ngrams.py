"""
More advanced n-gram models and more advanced selection of models
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
import numpy as np
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step2.csv')
data.head(3)
"""
Ok, so for features: 
We know we're using pre-review rating, restaurant price, review length, and mispelling count. 
For restaurant_type, we're going to bin that. We'll also remove restaurant_name as a predictive
variable (not really applicable to new restaurants). Finally, for the text, we're going to 
expand on our bag-of-words model by using lemmatization and TF-IDF for ngrams. 

Ok so instead of binning for the restaurant categories, we'll assign each one of them a normalized 
score based on average review rating for that category. For each restaurant (each of which may have
multiple categories) we average the scores of each of their categories to arrive at the restaurant's
"type_score" 
"""
restaurant_categories = pd.read_csv('../BIA660D_Group_1_Project/eda/type_data.csv')
restaurant_categories.sort_values(by='Average_Score', inplace=True, ascending=False)
restaurant_categories['Rank'] = range(1,len(restaurant_categories)+1)
restaurant_categories['Rank'] = restaurant_categories['Rank'].apply(lambda x: x / len(restaurant_categories)) #normalize
restaurant_categories
data['type_score'] = 0
for row_n in range(len(data)):
    raw_types = data['restaurant_type'][row_n]
    type_list = raw_types.strip("']").strip("['").split("', '")
    all_ranks = []
    for the_type in type_list:
        the_rank = restaurant_categories.iloc[np.where(restaurant_categories.iloc[:,0]==the_type)[0]]['Rank']
        all_ranks.append(the_rank.values[0])
    data.loc[row_n, 'type_score'] = np.mean(all_ranks)
data.head(3)
data.drop(columns=['restaurant_name', 'restaurant_type'], inplace=True)
data.to_csv('../BIA660D_Group_1_Project/eda/hoboken_step3.csv', index = False) #yay!
#################################
import pandas as pd
import numpy as np
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step3.csv')
data.head(3)
# Now for the hard part, the text.

